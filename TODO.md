# TODO


---

## - [X] Min Max Algorithim

- [X] Rework board class to track connections
   This will save a lot of compute time because
   new instances will not need to recheck entire board.
   Also gives info needed to draw the winning connection
   Puts blocked off chains into dead\_chains list
- [X] Static evalutations
   It would be really cool to have different evaluations
   and put them against each other.   
- [X] Minmax Implementation
- [X] Alpha / Beta Pruning
    - [X] Alpha / Beta pruning stop when a win is detected!!!
- [X] Integrate to work with GUI
- [X] Order optimization
   Figure out how to prioritize more interesting moves -
   probably will also be some sort of running total, getting
   updated with each move



---

## - [ ] UI / UX

- [ ] GUI for end\_screen
    - [ ] Display restart / tie text
    - [ ] Also for ties
    - [ ] Maybe have seperate pvp vs pve mode
    - [ ] Settings button during the game
    - [ ] Different difficulties
- [X] Have seperate modes between AI and user
~~- [ ] Connect to Pi to take button inputs~~
- [X] Display wins & winner
- [X] Animate AI choosing placement
- [X] Falling sound effect
- [ ] Play Sound for victory / loss
- [ ] Minor Cleanups
    - [X] Don't draw preview piece on top row
    - [ ] Make AI move piece around during thinking time,
       not just during animation at end
    - [ ] Diagnol connections, when drawn, are disconnected.
       add the little connectors to make them continous
