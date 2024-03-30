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
