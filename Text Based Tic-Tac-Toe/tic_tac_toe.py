# TODO-1, deal with the board presentation...
placeholder = [
    '-', '-', '-',
    '-', '-', '-',
    '-', '-', '-',
]


# function for displaying the board...
def print_playing_board():
    print('\n')
    print(placeholder[0] + "   |   " + placeholder[1] + "   |   " + placeholder[2], end='\n\n')
    print(placeholder[3] + "   |   " + placeholder[4] + "   |   " + placeholder[5], end='\n\n')
    print(placeholder[6] + "   |   " + placeholder[7] + "   |   " + placeholder[8], end='\n\n')


print_playing_board()
