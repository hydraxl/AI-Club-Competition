# Library Dependencies
from random import choice

# File Dependencies
from .display import *
from .run_player import *

# Takes in 2 player functions
# Returns the winner
    # 2 means player 2 wins
    # 1 means player 1 wins
    # 0 means there's a bug and the game is unfinished due to turn limit
    # -1 means tie
# Board format:
    # 5x5 list
    # 0 = unclaimed square
    # 1 = claimed by player looking at the square
    # -1 = claimed by opponent
def game(p1_function, p2_function, p1_name, p2_name, timeout=None, turn_limit=None, to_display_board=False, to_display_winner=False):
    # Initial Variables
    size = 5
    p1_board = [[0]*size for i in range(size)]
    p2_board = [[0]*size for i in range(size)]
    num_turns = 0

    # Runs player functions
    if timeout == None:
        run = run_player_no_timeout
    else:
        run = run_player

    # While game is ongoing
    while board_state(p1_board) == 0:
        # Check turn limit
        if num_turns == turn_limit:
            return 0
        num_turns += 1

        # Display board state if needed
        if to_display_board:
            display_board(p1_board)

        # Determine which player makes the next move
        player_turn = choice([1, 2])
        
        # Player 1
        if player_turn == 1:
            # Determine what position player 1 is selecting
            position = run(p1_function, p1_board, timeout)
            

            # Determine if position is valid
            if position == (-1, -1): # Player function timed out
                continue
            if p1_board[position[0]][position[1]] != 0: # Position is already taken
                continue
            
            # Adjust board state given new position
            p1_board[position[0]][position[1]] = 1
            p2_board[position[0]][position[1]] = -1
        
        # Player 2
        if player_turn == 2:
            # Determine what position player 1 is selecting
            position = run(p2_function, p2_board, timeout)
            

            # Determine if position is valid
            if position == (-1, -1): # Player function timed out
                continue
            if p2_board[position[0]][position[1]] != 0: # Position is already taken
                continue
            
            # Adjust board state given new position
            p1_board[position[0]][position[1]] = -1
            p2_board[position[0]][position[1]] = 1

        # Display board state if needed
        if to_display_board:
            display_board(p1_board)
        
    # Format results
    winner = board_state(p1_board)
    if winner == -1:
        winner = 0

    # Display Results
    if to_display_winner:
        display_winner(winner, p1_name, p2_name)
    
    # Return results
    return winner


# Returns an integer representing the state of the board
    # 2 means player 2 wins
    # 1 means player 1 wins
    # 0 means no winner has been determined
    # -1 means there is a tie
# Looks at board from p1 perspective
def board_state(p1_board):
    # Length of board
    size = len(p1_board)
    
    # If board is completely filled up
    board_full = True
    total_sum = 0

    # Diagonals
    sum_left_diagonal = 0
    sum_right_diagonal = 0
    for i in range(size):
        sum_left_diagonal += p1_board[i][i]
        sum_right_diagonal += p1_board[size - 1 - i][i]

        # Verticals and Horizontals
        sum_vertical = 0
        sum_horizontal = 0
        for j in range(size):
            total_sum += p1_board[i][j]
            if p1_board[i][j] == 0:
                board_full = False
            sum_horizontal += p1_board[j][i]
            sum_vertical += p1_board[i][j]
        
        # Check Verticals and Horizontals for winners
        if sum_horizontal == size:
            return 1
        if sum_horizontal == -size:
            return 2
        if sum_vertical == size:
            return 1
        if sum_vertical == -size:
            return 2
    
    # Check Diagonals for winners
    if sum_left_diagonal == size:
        return 1
    if sum_left_diagonal == -size:
        return 2
    if sum_right_diagonal == size:
        return 1
    if sum_right_diagonal == -size:
        return 2
    
    # If board is full, declare tie
    if board_full:
        return -1
    '''
    if board_full and total_sum > 0:
        return 1
    if board_full and total_sum < 0:
        return 2
    if board_full and total_sum == 0:
        return -1
    '''
    
    # No winner detected, game is still ongoing
    return 0