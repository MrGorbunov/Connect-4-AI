def turn(b, ind):
    b.editBoard(ind)
    b.update_connections([ind, 5 - b.empty_slots_in_col(ind)], b.turn % 2 + 1)
    b.changeTurn()
    b.printBoard()
    print('')



class Board():
    n = 0
    r = 1
    y = 2

    def __init__(self):
        self.row5 = [self.n, self.n, self.n, self.n, self.n, self.n, self.n]  # empty board creation
        self.row4 = [self.n, self.n, self.n, self.n, self.n, self.n, self.n]  # empty board creation
        self.row3 = [self.n, self.n, self.n, self.n, self.n, self.n, self.n]  # empty board creation
        self.row2 = [self.n, self.n, self.n, self.n, self.n, self.n, self.n]  # empty board creation
        self.row1 = [self.n, self.n, self.n, self.n, self.n, self.n, self.n]  # empty board creation
        self.row0 = [self.n, self.n, self.n, self.n, self.n, self.n, self.n]  # empty board creation

        self.boardState = [self.row0, self.row1, self.row2, self.row3, self.row4, self.row5]

        self.turn = 0
       
        #Instead of doing a full-board sweep everytime to check for a win / connections (minmax)
        #this array gets updated and keeps track of all connections of length 1 or higher
        #example: [ [1, [0,1], [1,1]],  [2, [0,0], [1,0], [2,0]] ]
        #1 or 2 refers to the color, each [col,row] pair is the actual pieces in the connection
        #this means that the win check is now just seeing if len(connections[i]) > 4
        self.connections = []
        #When a connection is surrounded on both ends by an opposing color, it becomes dead
        self.dead_connections = []

    def changeTurn(self):
        self.turn = self.turn + 1

    def empty_slots_in_col(self, col_ind):
        '''Returns the number of empty slots in column col_ind. Must be 0-6 (inclusive)'''
        empty_slots = 6

        for row in self.boardState:
            if row[col_ind] != self.n:
                empty_slots -= 1

        return empty_slots



    def get_chain(self, start_cord, direction, piece_value):
        '''Will iterate along direction and return any connections. Goes backwards and forwards'''
        #start_cord = [x, y]
        #direction = [dx, dy]
        #piece_value = 1, 2

        cur_cord = list(start_cord)
        #NOTE: the fact that the start_cord is index is 2 is used in update_connections
        #do not change that (or go change it there), and
        #the fact the the last index is the end of the iteration is used in get_dead_chain 
        cur_chain = [piece_value, start_cord]
        
        #if the starting piece is not the right color
        if self.boardState[cur_cord[1]][cur_cord[0]] != piece_value:
            return [0]

        for i in range(2):
            
            #this will iterate forward along direction, at most 4 times
            for j in range(4):
                cur_cord[0] += direction[0]
                cur_cord[1] += direction[1]

                #check if still on board
                if not (cur_cord[0] >= 0 and cur_cord[0] <= 6 and
                        cur_cord[1] >= 0 and cur_cord[1] <= 5):
                    break

                #check if the new cordinate is the same piece
                if self.boardState[cur_cord[1]][cur_cord[0]] != piece_value:
                    break
                
                #if both checks pass, then that means that this is a connection
                cur_chain.append(list(cur_cord))

            #after one loop, we want to invert the direction
            direction[0] *= -1
            direction[1] *= -1
            cur_cord = list(start_cord)

        #at the end, just return the chain 
        return cur_chain



    def get_dead_chain(self, start_cord, direction, piece_value):
        '''Will iterate along direction and return a chain if it has been blocked off. piece_value is of the chain. Assumes that one end is blocked off by default (in calling this function)'''
        cur_cord = list([start_cord[0] + direction[0], start_cord[1] + direction[1]])
        cur_chain = self.get_chain(cur_cord, direction, piece_value)

        #[1 or 2, cord] chains are not in connections, so can be ignored
        if len(cur_chain) <= 2:
            return [0]

        #because of the order of iteration, the last cord in cur_chain is in the direction of direction
        #so cur_chain[-1] + direction = cord of piece to check
        cord_to_check = [cur_chain[-1][0] + direction[0], cur_chain[-1][1] + direction[1]]
        blocked = False 

        if cord_to_check[0] > 6 or cord_to_check[0] < 0 or cord_to_check[1] > 5 or cord_to_check[1] < 0:
           return cur_chain 
        
        if self.boardState[cord_to_check[1]][cord_to_check[0]] != 0:
           return cur_chain

        return [0]

         

    def update_connections(self, piece_cord, piece_value):
        '''Will check for new connections at piece_cord and update internal connection list'''
        directions = [ [0,1], [1,1], [1,0] , [1, -1] ]

        for direct in directions:
            new_chain = self.get_chain(piece_cord, direct, piece_value)

            if len(new_chain) > 2:
                if len(new_chain) == 3:
                    #this is a completely new chain
                    self.connections.append(new_chain)
                    print("Alive: " + str(new_chain)) 
                    continue
                
                #looking for which chain to override 
                for old_chain in self.connections:
                    #checks if correct length and same piece values
                    if len(old_chain) == len(new_chain) - 1 and old_chain[0] == new_chain[0]: 
                           #[0] = piece_value, [1] = first piece of the check
                           #remove [1] from new_chain should leave same
                           #values as old_chain (different order though)
                           preserved_chain = new_chain 
                           new_chain = new_chain[2:]
                           old_chain = old_chain[1:]

                           #finding difference in the two
                           for cord in new_chain:
                               for old_cord in old_chain:
                                   if old_cord == cord:
                                       old_chain.remove(cord)
                                       print(old_cord)
                                       break
                          
                           #if there is 0 difference
                           if len(old_chain) == 0:
                              print("Alive: " + str(new_chain)) 
                              #this is the guy
                              self.connections.remove(preserved_chain[:1] + preserved_chain[2:])
                              self.connections.append(preserved_chain)

            #chain less than 2, check if just blocked something off
            else:

                other_value = 1
                if piece_value == 1:
                    other_value = 2

                #get_dead_chain will not invert direction, so we must check twice
                for i in range(2):
                   dead_chain = self.get_dead_chain(piece_cord, direct, other_value)
                   if dead_chain != [0]: 
                       print("Dead: " + str(dead_chain))
                       self.connections.remove(dead_chain)
                       self.dead_connections.append(dead_chain)

                   #inverting direction for the next iteration
                   direct[0] *= -1
                   direct[1] *= -1



     
    def isCompTurn(self):
        return self.turn % 2 == 0

    def editBoard(self, moveNumber):
        for i in range(0, len(self.boardState)):  # checks for each row in a column for empty space
            if self.boardState[i][moveNumber] == self.n:  # if the spot you want to place in is not occupied
                if self.isCompTurn():  # if it is player 1's turn
                    self.boardState[i][moveNumber] = self.r
                else:  # if it is player 2's turn
                    self.boardState[i][moveNumber] = self.y
                break

    def is_winner(self):
        '''Returns True if there is a winner'''
        for con in self.connections:
            if len(con) >= 5:
                return True

        return False

    def printBoard(self):
        print(self.row5)
        print(self.row4)
        print(self.row3)
        print(self.row2)
        print(self.row1)
        print(self.row0)
        print(" 1  2  3  4  5  6  7")
