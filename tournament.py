import random

# Object representing a tournament between players
#   Each type of tournament is represented as a generator method
class Tournament:
    def __init__(self):
        self.num_players = None
        self.last_winner = None
        self.last_loser = None
    
    # Single Game
    #   Pits the first player against themself once, then stops
    #   Used primarily for testing
    def testing_game(self):
        yield (0, 0)

    # Round Robin tournament
    #   Every player plays against every other player once
    def round_robin(self):
        for i in range(self.num_players):
            for j in range(i+1, self.num_players):
                yield i, j

    # Single Elimination tournament
    #   Run pairs of players against each other
    #   Winners move on to the next round
    #   Loses are out of the tournament
    #   Order is randomized
    def single_elimination(self):
        current_round = [i for i in range(self.num_players)]
        while (len(current_round)) > 1:
            # Shuffle players every round so nobody gets multiple byes
            random.shuffle(current_round)

            # Yield adjacent pairs, add winners to next round
            next_round = []
            for i in range(0, len(current_round) - 1, 2):
                yield (current_round[i], current_round[i+1])

                # Adds winner to next round
                #   Outside code sets self.last_winner between generator calls
                next_round.append(self.last_winner)
            
            # If there's an odd number of players
            #   the player that was skipped is added to the next round
            if len(current_round) % 2 == 1:
                next_round.append(current_round[-1])
            
            # Starts the next round
            current_round = next_round

# Determines winner of a series of games
#   Returns whichever player had more total wins
#   If there is a tie, chooses randomly
#   Required for tournament structures that do not allow for ties
def determine_overall_winner(p1_wins, p2_wins, ties):
    if p1_wins > p2_wins:
        return 1
    elif p2_wins > p1_wins:
        return 2
    else:
        return random.choice([1, 2])
