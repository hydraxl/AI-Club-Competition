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