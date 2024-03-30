### IMPORTANT SYNTAX ###
# Connect 4 Board is represented as a 2d list
# Syntax for accessing the value of the board at a given position: board[x][y]
# x=0 is the far left of the board
# y=0 is the bottom of the board
# The board is 7 squares wide and 6 squares tall
# Your algorithm should return a single integer representing an x coordinate
#
# You MUST have a string called "programmer_name"
# Your algorithm MUST be named "game_player"
# Your algorithm MUST take in a single input, preferably called "board"
#
# All of your code MUST be contained in a single .py file


# Name of the programmer
programmer_name = "Adam Freed"

# Algorithm for playing the game
def game_player(board):
    NUM_COLUMNS = 7
    NUM_ROWS = 6

    MY_TILE = 1
    EMPTY_TILE = 0
    OPPONENT_TILE = -1

    for y in range(NUM_ROWS):
        for x in range(NUM_COLUMNS):
            if board[x][y] == EMPTY_TILE:
                return x