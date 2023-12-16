# TODO-1, deal with the board presentation...
placeholder = [
    '-', '-', '-',
    '-', '-', '-',
    '-', '-', '-',
]


# function for displaying the board...
def print_playing_board():
    print('\nHorizontally, each "-" refers to numbers 1-9 from top left to bottom right.')
    print('\n')
    print(placeholder[0] + '   |   ' + placeholder[1] + '   |   ' + placeholder[2], end='\n\n')
    print(placeholder[3] + '   |   ' + placeholder[4] + '   |   ' + placeholder[5], end='\n\n')
    print(placeholder[6] + '   |   ' + placeholder[7] + '   |   ' + placeholder[8], end='\n\n')


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

        return 'win'

    # checking for draw...
    elif '-' not in placeholder:
        return 'tie'

    # last case, game's not over so play on...
    else:
        return 'play'


# TODO-3, dealing with player turns...
def play_turns(x_or_o):
    print(f'{x_or_o}\'s turn...')
    # taking user input...
    location = int(input('To play, select a position among (1-9): -> '))

    # checking if the user entered a valid input...
    while location not in range(1, 10):
        location = int(input('Invalid input, only enter position numbers from 1 to 9. -> '))

    # checking if the place is used-up...
    while placeholder[location - 1] != '-':
        location = int(input('Position is already taken, choose another one. -> '))

    placeholder[location - 1] = x_or_o
    print_playing_board()


# TODO-4, make a function to run the game...
def game_play():
    print_playing_board()
    playing_as = 'x'

    game_is_on = True
    while game_is_on:
        play_turns(playing_as)
        game_result = check_stats()

        if game_result == 'win':
            print(f'{playing_as} wins!')
            game_is_on = False

        elif game_result == 'tie':
            print('It\'s a Tie!')
            game_is_on = False

        else:
            playing_as = 'o' if playing_as == 'x' else 'x'


if __name__ == '__main__':
    game_play()
