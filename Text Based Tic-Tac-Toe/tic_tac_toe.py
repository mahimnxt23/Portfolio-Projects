# TODO-1, deal with the board presentation...
placeholder = [
    '-', '-', '-',
    '-', '-', '-',
    '-', '-', '-',
]


# function for displaying the board...
def print_playing_board():
    print('\nHorizontally, each "-" refers to numbers from 1-9 from top left to bottom right. To play, select a '
          'position among (1-9): -> ')
    print('\n')
    print(placeholder[0] + '   |   ' + placeholder[1] + '   |   ' + placeholder[2], end='\n\n')
    print(placeholder[3] + '   |   ' + placeholder[4] + '   |   ' + placeholder[5], end='\n\n')
    print(placeholder[6] + '   |   ' + placeholder[7] + '   |   ' + placeholder[8], end='\n')


# TODO-2, dealing with win/lose/draw conditions...
def check_stats():
    # checking for win...
    if (
            # firstly, check horizontal winning possibilities...
            (placeholder[0] == placeholder[1] == placeholder[2] != '-') or
            (placeholder[3] == placeholder[4] == placeholder[5] != '-') or
            (placeholder[6] == placeholder[7] == placeholder[8] != '-') or

            # secondly, check vertical winning possibilities...
            (placeholder[0] == placeholder[3] == placeholder[6] != '-') or
            (placeholder[1] == placeholder[4] == placeholder[7] != '-') or
            (placeholder[2] == placeholder[5] == placeholder[8] != '-') or

            # lastly, check diagonal winning possibilities...
            (placeholder[0] == placeholder[4] == placeholder[8] != '-') or
            (placeholder[2] == placeholder[4] == placeholder[6] != '-')):

        return 'You Win!'

    # checking for draw...
    elif '-' not in placeholder:
        return 'It\'s Tie.'

    # last case, game's not over so play on...
    else:
        return 'Continue to make your move.'


# TODO-3, dealing with player turns...


# TODO-4, make a function to run the game...

if __name__ == '__main__':
    print_playing_board()
