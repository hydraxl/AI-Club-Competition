# Library Dependencies
from random import choice

# File Dependencies
from .run_player import *
from .display import *

# Board Info Variables
NUM_COLUMNS = 7
NUM_ROWS = 6
WIN_NUM = 4
EMPTY_TILE = 0
P1_TILE = 1
P2_TILE = -1

# Board State Variables
ONGOING = -1
TIE = 0
P1_WIN = 1
P2_WIN = 2

def game(p1_function, p2_function, p1_name, p2_name, timeout=None, max_timeouts=None, to_display_board=False, to_display_winner=False):
    # Determine which player moves first randomly
    is_p1_turn = choice([True, False])

    # Set up board
    p1_board = [[EMPTY_TILE]*NUM_ROWS for i in range(NUM_COLUMNS)]
    p2_board = [[EMPTY_TILE]*NUM_ROWS for i in range(NUM_COLUMNS)]

    # How many turns have passed
    num_timeouts = 0

    # Handler function for player functions
    if timeout == None:
        run = run_player_no_timeout
    else:
        run = run_player_with_timeout


    # Run game
    while board_state(p1_board) == ONGOING:
        # Check turn limit
        if num_timeouts == max_timeouts:
            return TIE

        # Current player makes their play
        if is_p1_turn:
            x = run(p1_function, p1_board, timeout)
            tile = P1_TILE
        else:
            x = run(p2_function, p2_board, timeout)
            tile = P2_TILE
        
        # If player timed out, skip their turn
        if x == DEFAULT_TIMEOUT_VALUE:
            num_timeouts += 1
            continue
        
        # Place tile on first empty square in selected column
        for y in range(NUM_ROWS):
            if p1_board[x][y] == EMPTY_TILE:
                p1_board[x][y] = tile
                p2_board[x][y] = -tile
                break
        
        # If needed, display board
        if to_display_board:
            display_board(p1_board)
        
        # Switch turns
        is_p1_turn = not is_p1_turn
    
    # Determine winner
    winner = board_state(p1_board)
    
    # Display winner if needed
    if to_display_winner:
        display_winner(winner, p1_name, p2_name)
    
    # Return results
    return winner


def board_state(board):

    # Is the board filled
    board_is_filled = True
    
    # Number of tiles in a row for each direction
    # Vertical
    vertical_p1 = 0
    vertical_p2 = 0
    
    # Horizontal
    horizontal_p1 = 0
    horizontal_p2 = 0

    # Up-right diagonal
    right_diagonal_p1 = True
    right_diagonal_p2 = True

    # Up-left diagonal
    left_diagonal_p1 = True
    left_diagonal_p2 = True

    # Check verticals
    for x in range(NUM_COLUMNS):
        for y in range(NUM_ROWS):
            # Vertical is empty from this point
            if board[x][y] == EMPTY_TILE:
                # There is at least 1 empty square on the board
                board_is_filled = False
                break

            # P1 has placed in the spot
            elif board[x][y] == P1_TILE:
                vertical_p1 += 1
                vertical_p2 = 0
            
            # P2 has placed in the spot
            elif board[x][y] == P2_TILE:
                vertical_p1 = 0
                vertical_p2 += 1
            
            # Check for wins
            if vertical_p1 == WIN_NUM:
                return P1_WIN
            elif vertical_p2 == WIN_NUM:
                return P2_WIN
        
        # Next column, reset values
        vertical_p1 = 0
        vertical_p2 = 0
   
    # Check horizontals
    for y in range(NUM_ROWS):
        for x in range(NUM_COLUMNS):
            # Spot is empty
            if board[x][y] == EMPTY_TILE:
                horizontal_p1 = 0
                horizontal_p2 = 0
            
            # P1 has placed in the spot
            elif board[x][y] == P1_TILE:
                horizontal_p1 += 1
                horizontal_p2 = 0
            
            # P2 has placed in the spot
            elif board[x][y] == P2_TILE:
                horizontal_p1 = 0
                horizontal_p2 += 1
            
            # Check for wins
            if horizontal_p1 == WIN_NUM:
                return P1_WIN
            elif horizontal_p2 == WIN_NUM:
                return P2_WIN
        
        # Next row, reset values
        horizontal_p1 = 0
        horizontal_p2 = 0
    
    # Check diagonals
    for base_x in range(NUM_COLUMNS - WIN_NUM + 1):
        for base_y in range(NUM_ROWS - WIN_NUM + 1):
            # Check the entire up-right facing diagonal starting at (base_x, base_y)
            # Check the entire up-left facing diagonal starting at (NUM_COLUMNS - 1 - base_x, base_y)
            for n in range(WIN_NUM):
                right_diagonal_tile = board[base_x + n][base_y + n]
                left_diagonal_tile = board[NUM_COLUMNS - 1 - base_x - n][base_y + n]

                # Check for breaks in a 4-in-a-row
                # If a single tile doesn't match, set the value for that diagonal to fales
                if right_diagonal_tile != P1_TILE:
                    right_diagonal_p1 = False
                
                if right_diagonal_tile != P2_TILE:
                    right_diagonal_p2 = False
                
                if left_diagonal_tile != P1_TILE:
                    left_diagonal_p1 = False
                
                if left_diagonal_tile != P2_TILE:
                    left_diagonal_p2 = False

            # Check for wins
            if right_diagonal_p1 or left_diagonal_p1:
                return P1_WIN
            elif right_diagonal_p2 or left_diagonal_p2:
                return P2_WIN
            
            # Next position, reset values
            right_diagonal_p1 = True
            right_diagonal_p2 = True
            left_diagonal_p1 = True
            left_diagonal_p2 = True

    # Check if game is finished
    if board_is_filled:
        return TIE
    
    # If nothing triggered return, game is still ongoing
    return ONGOING
