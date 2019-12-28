PIECE = {
    "YEL": 2,
    "RED": 1,
    "AIR": 0,
    "WALL": 3
}


def array_dif (arr1, arr2):
    diff = list(arr1)

    for a in arr1:
        for b in arr2:
            if a == b:
                diff.remove(a)

    return diff



#
# actual class
#

class Board():
    def __init__(self):
        self.board_state = []

        for row in range(6):
            self.board_state += [[]]
            for col in range(7):
                self.board_state[row] += [PIECE['AIR']]

        self.turn = 0
       
        #Instead of doing a full-board sweep everytime to check for a win / connections (minmax)
        #this array gets updated and keeps track of all connections of length 1 or higher
        #example: [ [1, [0,1], [1,1]],  [2, [0,0], [1,0], [2,0]] ]
        #1 or 2 refers to the color, each [col,row] pair is the actual pieces in the connection
        #this means that the win check is now just seeing if len(connections[i]) > 4
        self.connections = []
        #When a connection is surrounded on both ends by an opposing color, it becomes _ead
        self.dead_connections = []


    def change_turn(self):
        self.turn += 1


    def handle_turn(self, move_ind, print_to_console = False):
        '''Calls everything necessary to process one turn, returns True if valid move'''
        if self.edit_board(move_ind):
            self.update_connections([move_ind, 5 - self.empty_slots_in_col(move_ind)])
            self.change_turn()

            if print_to_console:
                self.print_board()

            return True

        return False

    

    def empty_slots_in_col(self, col_ind):
        '''Returns the number of empty slots in column col_ind. Must be 0-6 (inclusive)'''
        empty_slots = GAME_STATE.COLUMN

        for row in self.board_state:
            if row[col_ind] != PIECE['AIR']:
                empty_slots -= 1

        return empty_slots


    def iterate_along(self, start_cord, direction, piece_value):
        '''Returns the cords of a chain and what stopped it; 0=air, 1,2=piece, 3=wall; assumes inputs are correct'''
        cur_val = piece_value
        cur_cord = list(start_cord)
        return_list = [0, start_cord]

        while (cur_val == piece_value): 
            cur_cord[0] += direction[0] 
            cur_cord[1] += direction[1]

            if (cur_cord[0] < 0 or cur_cord[0] > 6 or
                cur_cord[1] < 0 or cur_cord[1] > 5):
                cur_val = PIECE['WALL']
                break


            cur_val = self.board_state[cur_cord[1]][cur_cord[0]]

            if cur_val != piece_value:
                break

            return_list += [list(cur_cord)]


        return_list[0] = cur_val
        return return_list


    def update_connections(self, piece_cord):
        '''Will check for new connections at piece_cord and update internal connection list'''
        piece_value = self.board_state[piece_cord[1]][piece_cord[0]]
   
        #have this handy
        other_piece = PIECE['YEL']
        if piece_value == PIECE['YEL']:
            other_piece = PIECE['RED']
        
        center_cord = piece_cord
        dirs = [[0,1], [1,1], [1,0], [-1,1]]

        for direc in dirs:
            alt_direc = [direc[0] * -1, direc[1] * -1]
            
            #this gather a connection going in bothe directions
            connection = self.iterate_along(center_cord, direc, piece_value)
            other_con = self.iterate_along(center_cord, alt_direc, piece_value)
            true_con = [piece_value] + connection[1:] + other_con[2:]

            #we don't care about length 1 "connection" i.e. solo pieces
            if len(true_con) > 2:
                winning_con =      len(true_con) >= 5
                free_one_side =    connection[0] == 0
                free_other_side =  other_con[0] == 0
                
                if free_one_side or free_other_side or winning_con:
                    self.add_to_connections(true_con)

                else:
                    #this connection is blocked off
                    self.add_dead_connection(true_con)
                     

            #check for having blocked the other piece
            #connection[0] indicates what's at the end of the chain
            if len(connection) <= 2:
                if connection[0] != PIECE['WALL'] and connection[0] != PIECE['AIR']:
                    self.check_for_blocking(center_cord, direc, other_piece)
            
            if len(other_con) <= 2:
                if other_con[0] != PIECE['WALL'] and other_con[0] != PIECE['AIR']:
                    self.check_for_blocking(center_cord, alt_direc, other_piece)



    def check_for_blocking(self, center, direction, other_piece):
        '''Checks if the end of the chain along direction is blocked'''
        offset_cord = [center[0] + direction[0], center[1] + direction[1]]
        enemy_chain = self.iterate_along(offset_cord, direction, other_piece)

        if enemy_chain[0] != PIECE['AIR']:
            #just got blocked off
            self.add_dead_connection([other_piece] + enemy_chain[1:])



    def add_dead_connection(self, connection):
        '''Will remove the conncetion from connections, and add it to dead connections'''
        # < 5 prevents winning connections from being removed
        if len(connection) >= 5:
            return

        for con in self.connections:
            if len(array_dif(con, connection)) == 0:
                self.connections.remove(con)
                self.dead_connections += [con]




    def add_to_connections(self, connection):
        '''Will remove the old connection, and add the new one'''
        if len(connection) == 2: 
            return
        elif len(connection) == 3:
            self.connections += [connection]
            return

        for old_con in self.connections:
            #must go out and find the old connection to replace
            if len(old_con) != len(connection) - 1:
                continue

            #important that old_con is first
            diff = array_dif(old_con, connection)

            if len(diff) != 0:
                continue

            self.connections.remove(old_con)
            self.connections += [connection]
            return
       
        #possible that this was X _ X => X X X
        #hence why adding even if no previous connection was found
        self.connections += [connection]

     
    def is_comp_turn(self):
        return self.turn % 2 == 0


    def edit_board(self, move_number):
        '''Adds a piece in the column move_number. Returns True if successful'''
        for i in range(0, len(self.board_state)):    
            if self.board_state[i][move_number] == PIECE['AIR']:
            
                if self.is_comp_turn():  
                    self.board_state[i][move_number] = PIECE['RED']
                else:  
                    self.board_state[i][move_number] = PIECE['YEL']
               
                return True

        return False


    def is_winner(self):
        '''Returns whether or not there is a winner'''
        for con in self.connections:
            if len(con) >= 5:
                return True

        return False


    def is_tie(self):
        '''Checks if currently a tie, returns True if it is a tie'''
        all_filled = True

        for col in self.board_state:
            for p in col:
                if p == PIECE['AIR']:
                    all_filled = False

        return all_filled and not self.is_winner() 


    def get_winning_connection(self):
        '''Returns the winning connection [1, cord, ...] if there is a winner,
        otherwise returns []'''
        for con in self.connections:
            if len(con) >= 5:
                return con

        return []


    def print_board(self):
        for row_ind in range(5, -1, -1):
            row = self.board_state[row_ind]

            for piece in row:
                if piece == 0:
                    print "| ",
                else:
                    print "|" + str(piece),
            print ""

        print(" 0  1  2  3  4  5  6 ")

