# Command Line
main command: python3 main.py GameName *args  
example command: python3 main.py Connect4 -dg -out=results.csv -tournament=testing_game  
arguments:  
  * dg                   — enables text display of game boards during games  
  * dw                   - enables text display of game winners  
  * out=(string)         — stores results into a file with a given name (PLEASE USE ".csv" file extension)  
  * n=(int)              — sets the number of games played in a single round  
  * timeout=(int)        — sets how long a player function can run before timing out (default is infinite)  
  * timeout_limit=(int)  — sets the maximum number of times a player can timeout before losing (default is infinite)  
  * tournament=          — sets the tournament settings
    * testing_game           - only plays a single game, player 1 against themself. Primarily for testing
    * round_robin            - every player plays against every other player
    * single_elimination     - pairs players, losers are eliminated, repeats  

# Player Files  
player files must be placed in a folder called "player_functions"  
player files must end in ".py" and be written in python  
player files must contain a string variable called "programmer_name" represents the name of the programmer or team
player files must contain a function called "game_player"  
  * input represents the state of the game
  * output represents the move they'd make on the board  

# Game Path
path variable leading to a game folder  
game folder must contain a file called "game.py"  
game file must contain a series of global variables representing the outcome of a game  
  * TIE     - Game resulted in a tie
  * P1_WIN  - Player 1 won
  * P2_WIN  - Player 2 won  
game file must contain a function called "game"
  * input:
    * p1_function       — game_player function from a player file
    * p2_function       — game_player function from a player file
    * p1_name           - name for player 1
    * p2_name           - name for player 2
    * timeout           - maximum amount of time a player function can use (default value of None)
    * timeout_limit     - maximum number of times a player can timeout before losing (default value of None)
    * to_display_board  - boolean of whether board state should be actively displayed during game
    * to_display_winner - boolean of whether winner should be displayed at the end of each game
  * output:
    * TIE     - tie game
    * P1_WIN  - player 1 wins
    * P2_WIN  - player 2 wins  

# Output
Outputs results to a CSV file  
Format: p1_name, p2_name, p1_wins, p2_wins, ties  
