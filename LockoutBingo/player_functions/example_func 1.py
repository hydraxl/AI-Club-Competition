# Name of the programmer
programmer_name = "Example 1"

# Algorithm for playing the game
def game_player(board):
    size = len(board)
    for x in range(size):
        for y in range(size):
            if board[x][y] == 0:
                return (x, y)