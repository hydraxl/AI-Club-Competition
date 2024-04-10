# Name of the programmer
programmer_name = "Adam Freed"

# Useful Variables
X_SIZE = 7
Y_SIZE = 6

MY_TILE = 1
EMPTY_TILE = 0
OPPONENT_TILE = -1




# Algorithm for playing the game
def game_player(board):
    # Takes in a 7x6 board 
    # Y
    # |   ---------------
    # 5  | 0 0 0 0 0 0 0 |
    # 4  | 0 0 0 0 0 0 0 |
    # 3  | 0 0 0 0 0 0 0 |
    # 2  | 0 0 0 0 0 0 0 |
    # 1  | 0 0 0 0 0 0 0 |
    # 0  | 0 0 0 0 0 0 0 |
    # |   ---------------
    #   -- 0 1 2 3 4 5 6 -- X

    # Format to look at a specific position: board[x][y]
    # Values at a specific position:
    #    0 -> empty
    #    1 -> your tile
    #   -1 -> opponent tile
    for y in range(Y_SIZE):
        for x in range(X_SIZE):
            if board[x][y] == EMPTY_TILE:
                return x


### Useful Algorithms ###

# Returns true if you went first
# Works by counting the number of your tiles and your opponent's tiles
# If you have the same number of tiles as your opponent, you went first
# If your opponent has more tiles, you went second
def am_I_first(board):
    tile_sum = 0
    for y in range(Y_SIZE):
        for x in range(X_SIZE):
            tile_sum += board[x][y]
    
    if tile_sum == 0:
        return True
    elif tile_sum == -1:
        return False