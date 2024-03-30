def display_board(board):
    size = 5
    endc = '\033[0;0m'
    red = '\033[0;;41m'
    blue = '\033[0;;44m'
    empty_row = '|' + ' '*(size*4) + '|'
    for i in range(size):
        new_row = '| '
        for j in range(size):
            val = str(round(board[j][i]))
            if val == '1':
                new_row += blue
            elif val == '-1':
                new_row += red
            new_row += '  ' + endc + ' '
            if j == size - 1:
                new_row += '|'
            else:
                new_row += ' '
        print(new_row)
        if i != size - 1:
            print(empty_row)
    print('\n\n')

def display_winner(outcome, p1_name, p2_name):
    if outcome == 2:
        print(f"{p2_name} defeats {p1_name}")
    elif outcome == 1:
        print(f"{p1_name} defeats {p2_name}")
    elif outcome == 0:
        print(f"{p1_name} and {p2_name} tie!")
    else:
        print(f"Something went wrong in the match between {p1_name} and {p2_name}")