import multiprocessing

# Callable object for multiprocessing
class Player_Func(object):
    # Initializes with player function
    def __init__(self, func):
        self.func = func
    
    # When called, takes in an input and 2 output variables
        # Runs player function and pushes results to output variables
    def __call__(self, input, x, y):
        result = self.func(input)
        x.value = result[0]
        y.value = result[1]


# Runs player function
    # If player function finishes in time, returns its output
    # If player function runs times out, returns None
    # Assumes output is in the format (x, y)
def run_player(func, input, timeout=1):
    # results of player function get pushed to result variable instead of returned
    x = multiprocessing.Value('i', -1)
    y = multiprocessing.Value('i', -1)
    
    # Start player function as a process
    f = Player_Func(func)
    p = multiprocessing.Process(target=f, args=(input, x, y))
    p.start()

    # Wait until process finishes or timeout
    p.join(timeout)

    # If process is still going, kill it
    if p.is_alive():
        p.terminate()
    
    # Return result
    return (x.value, y.value)

def run_player_no_timeout(func, input, timeout=None):
    return func(input)