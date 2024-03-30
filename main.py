### Command Line ###
# main command: python3 main.py GameName *args
# example command: python3 main.py Connect4 -dg -out=results.csv -tournament=testing_game
# arguments:
    # -dg                   — enables text display of game boards during games
    # -dw                   - enables text display of game winners
    # -out=(string)         — stores results into a file with a given name (PLEASE USE ".csv")
    # -n=(int)              — sets the number of games played in a single round
    # -timeout=(int)        — sets how long a player function can run before timing out (default is infinite)
    # -timeout_limit=(int)  — sets the maximum number of times a player can timeout before losing (default is infinite)
    # -tournament=          — sets the tournament settings
        # testing_game           - only plays a single game, player 1 against themself. Primarily for testing
        # round_robin            - every player plays against every other player
        # single_elimination     - pairs players, losers are eliminated, repeats

### Player Files ###
# player files must be placed in a folder called "player_functions"
# player files must end in ".py" and be written in python
# player files must contain a string variable called "programmer_name"
#   represents the name of the programmer or team
# player files must contain a function called "game_player"
#   input represents the state of the game
#   output represents the move they'd make on the board

### Game Path ###
# path variable leading to a game folder
# game folder must contain a file called "game.py"
# game file must contain a series of global variables representing the outcome of a game
#   TIE     - Game resulted in a tie
#   P1_WIN  - Player 1 won
#   P2_WIN  - Player 2 won
# game file must contain a function called "game"
#   input:
#       p1_function           — game_player function from a player file
#       p2_function           — game_player function from a player file
#       p1_name           - name for player 1
#       p2_name           - name for player 2
#       timeout           - maximum amount of time a player function can use (default value of None)
#       timeout_limit     - maximum number of times a player can timeout before losing (default value of None)
#       to_display_board  - boolean of whether board state should be actively displayed during game
#       to_display_winner - boolean of whether winner should be displayed at the end of each game
#   output:
#       TIE     - tie game
#       P1_WIN  - player 1 wins
#       P2_WIN  - player 2 wins

### Output ###
# Outputs results to a CSV file called "results.csv"
# Format: p1_name, p2_name, p1_wins, p2_wins, ties

# Library Dependencies
import importlib.util
import os
import sys

# File Dependencies
import tournament
from store_results import store_results

# Converts string syntax from path variable to import variable
def path_to_import(path):
    import_str = ''
    for c in path:
        # Filetype is not written
        if c == '.':
            break
        # Subdirectories are demarcated with '.' instead of '/'
        elif c == '/':
            import_str += '.'
        # Everything else is unchanged
        else:
            import_str += c
    return import_str

if __name__ == "__main__":
    # File system variables
    PLAYER_FUNCTION_FOLDER = "player_functions"
    GAME_FUNCTION_FOLDER = path_to_import(sys.argv[1])

    # Settings Defaults
    to_display_board = False
    to_display_winner = False
    output_file_name = None
    timeout = None
    turn_limit = None
    num_games = 1
    tournament_obj = tournament.Tournament()
    tournament_function = tournament_obj.round_robin

    # Find Game Function
    game_file = importlib.import_module(f"{GAME_FUNCTION_FOLDER}.game")
    game = game_file.game

    # Check flags for settings changes
    for arg in  sys.argv[2:]:
        if arg == "-dg":
            to_display_board = True
        elif arg == "-dw":
            to_display_winner = True
        elif arg[:5] == "-out=":
            output_file_name = f"{arg[5:]}"
        elif arg[:3] == "-n=":
            num_games = int(arg[3:])
        elif arg[:9] == "-timeout=":
            timeout = int(arg[9:])
        elif arg[:12] == "-turn_limit=":
            turn_limit = int(arg[12:])
        elif arg[:12] == "-tournament=":
            tournament_function = getattr(tournament_obj, arg[12:])

    # Grab data from player files
    player_function_filenames = os.listdir(f"./{GAME_FUNCTION_FOLDER}/{PLAYER_FUNCTION_FOLDER}")
    player_names = [] # Programmer names
    player_functions = [] # Player functions
    for filename in player_function_filenames:
        # Only check .py files
        if filename[-3:] != '.py':
            continue
        
        # Grab data
        file = importlib.import_module(f"{GAME_FUNCTION_FOLDER}.{PLAYER_FUNCTION_FOLDER}.{filename[:-3]}")
        player_names.append(file.programmer_name)
        player_functions.append(file.game_player)
    
    # Update tournament object with number of players
    tournament_obj.num_players = len(player_names)  

    # Run the tournament
    tournament_generator = tournament_function()
    for p1, p2 in tournament_generator:

        # Determine player information
        p1_name = player_names[p1]
        p2_name = player_names[p2]

        p1_function = player_functions[p1]
        p2_function = player_functions[p2]

        # Run the game and tally wins
        p1_wins = 0
        p2_wins = 0
        ties = 0
        for n in range(num_games):
            # Run a single game
            winner = game(p1_function, p2_function, p1_name, p2_name, timeout, turn_limit, to_display_board, to_display_winner)
            
            # Tally wins
            if winner == 0:
                ties += 1
            elif winner == 1:
                p1_wins += 1
            elif winner == 2:
                p2_wins += 1

        # Record results    
        if output_file_name != None:
            store_results(output_file_name, p1_name, p2_name, p1_wins, p2_wins, ties)
        
        # Pass results to tournament structure
        overall_winner = tournament.determine_overall_winner(p1_wins, p2_wins, ties)
        if overall_winner == 1:
            tournament_obj.last_winner = p1
            tournament_obj.last_loser = p2
        elif overall_winner == 2:
            tournament_obj.last_winner = p2
            tournament_obj.last_loser = p1
