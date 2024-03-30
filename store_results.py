import pandas as pd
import os.path

def store_results(filename, p1_name, p2_name, p1_wins, p2_wins, ties):
    # Formatting data to be stored
    data = f"\n{p1_name}, {p2_name}, {p1_wins}, {p2_wins}, {ties}"
    
    # Appending to file (and creating file if it doesn't exist)
    if os.path.isfile(filename):
        fd = open(filename, 'a')
    else:
        fd = open(filename, 'w')
        fd.write("p1_name, p2_name, p1_wins, p2_wins, ties")
    fd.write(data)
    fd.close()