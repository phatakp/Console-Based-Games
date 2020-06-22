"""
A Classic Tic Tac Toe game where two players compete on a grid.

Steps to Play:

1. Game displays a Tic Tac Toe (3x3 grid) and the corresponding position numbers of the grid.
2. Players are named Player-X and Player-O based.
3. Players get alternating turns. Default starting player is Player-X
4. Game asks for position number of the grid as input.
5. For all valid inputs, player's corresponding symbol is placed on the grid.
6. Game continues until any player wins or it ends in draw
"""
from os import name, system


class Box:
    """
    A class to represent a Box of TicTacToe

    """

    def __init__(self: object, pos: int, val: str) -> object:
        """
        Constructs all necessary attributes of Box object

        Parameters
        - - - - - -
        pos: Integer value ranging from 0 to 8
            Position of the box
        val: String value that stores X or O
            Player Move value
        """
        self.pos = pos
        self.val = val
        self.position_lines = self.get_position_line()
        self.value_lines = self.get_value_line()

    def get_position_line(self: object) -> list:
        """
        Returns a list of str lines depicting how the box positions will be printed on console
        """
        if self.pos == 0:
            line = [(' ' * 3 + "|"),
                    (f'{self.pos:^3}' + '|'),
                    ('-' * 3 + '┘'), ]
        elif self.pos == 1:
            line = [(' ' * 3),
                    (f'{self.pos:^3}'),
                    ('-' * 3), ]
        elif self.pos == 2:
            line = [('|' + ' ' * 3),
                    ('|' + f'{self.pos:^3}'),
                    ('└' + '-' * 3), ]
        elif self.pos == 3:
            line = [(' ' * 3 + '|'),
                    (f'{self.pos:^3}' + '|'),
                    (' ' * 3 + '|'), ]
        elif self.pos == 4:
            line = [(' ' * 3),
                    (f'{self.pos:^3}'),
                    (' ' * 3)]
        elif self.pos == 5:
            line = [('|' + ' ' * 3),
                    ('|' + f'{self.pos:^3}'),
                    ('|' + ' ' * 3), ]
        elif self.pos == 6:
            line = [('-' * 3 + '┐'),
                    (f'{self.pos:^3}' + '|'),
                    (' ' * 3 + '|'), ]
        elif self.pos == 7:
            line = [('-' * 3),
                    (f'{self.pos:^3}'),
                    (' ' * 3), ]
        else:
            line = [('┌' + '-' * 3),
                    ('|' + f'{self.pos:^3}'),
                    ('|' + ' ' * 3), ]
        return line

    def get_value_line(self: object) -> list:
        """
        Returns a list of str lines depicting how the box values will be printed on console
        """

        if self.pos == 0:
            line = [(' ' * 3 + "|"),
                    (f'{self.val:^3}' + '|'),
                    ('-' * 3 + '┘'), ]
        elif self.pos == 1:
            line = [(' ' * 3),
                    (f'{self.val:^3}'),
                    ('-' * 3), ]
        elif self.pos == 2:
            line = [('|' + ' ' * 3),
                    ('|' + f'{self.val:^3}'),
                    ('└' + '-' * 3), ]
        elif self.pos == 3:
            line = [(' ' * 3 + '|'),
                    (f'{self.val:^3}' + '|'),
                    (' ' * 3 + '|'), ]
        elif self.pos == 4:
            line = [(' ' * 3),
                    (f'{self.val:^3}'),
                    (' ' * 3)]
        elif self.pos == 5:
            line = [('|' + ' ' * 3),
                    ('|' + f'{self.val:^3}'),
                    ('|' + ' ' * 3), ]
        elif self.pos == 6:
            line = [('-' * 3 + '┐'),
                    (f'{self.val:^3}' + '|'),
                    (' ' * 3 + '|'), ]
        elif self.pos == 7:
            line = [('-' * 3),
                    (f'{self.val:^3}'),
                    (' ' * 3), ]
        else:
            line = [('┌' + '-' * 3),
                    ('|' + f'{self.val:^3}'),
                    ('|' + ' ' * 3), ]
        return line

    def set_value(self: object, val: str) -> None:
        """
        Sets the input value for current box object

        Parameters:
        - - - - - -
        val: str value to be set at position

        """
        self.val = val
        self.position_lines = self.get_position_line()
        self.value_lines = self.get_value_line()


class Grid:
    """
    A class to represent a 3x3 grid of TicTacToe
    Contains 9 individual box objects
    """

    def __init__(self: object) -> object:
        """
        Constructs all necessary attributes of Grid object

        """

        self.grid = [Box(row * 3 + col, ' ')
                     for row in range(3)
                     for col in range(3)]
        self.row_col_diagonal()

    def row_col_diagonal(self: object) -> None:
        """
        Sets list of values for each row, column and diagonal of the grid

        """
        self.rows = [[] for _ in range(3)]
        self.cols = [[] for _ in range(3)]
        self.diag = [[] for _ in range(2)]
        for box in self.grid:
            self.rows[box.pos // 3].append(box.val)
            self.cols[box.pos % 3].append(box.val)
            if box.pos % 4 == 0:
                self.diag[0].append(box.val)
            if box.pos in (2, 4, 6):
                self.diag[1].append(box.val)

    def set_value(self: object, pos: int, val: str) -> None:
        """
        Sets value of given grid box position

        Parameters
        - - - - - -
        pos: Position of the grid box
        val: Value to be set

        """
        self.grid[pos].set_value(val)
        self.row_col_diagonal()

    def print_grid(self: object) -> None:
        """
        Prints the grid of positions and values in 3x3 matrix

        """
        screen_clear()
        print('\n\t\tTIC-TAC-TOE\t\t Positions\n')

        lines = [[] for i in range(9)]

        # Indentation for better display
        for line in lines:
            line.append('\t\t')

        # Prints the grid with values of player moves
        for box in self.grid:
            index = box.pos // 3 * 3
            for line in box.value_lines:
                lines[index].append(str(line))
                index += 1

        # Indentation for better display
        for line in lines:
            line.append('\t\t')

        # Prints the grid with position of boxes
        for box in self.grid:
            index = box.pos // 3 * 3
            for line in box.position_lines:
                lines[index].append(str(line))
                index += 1

        boxes = '\n'.join([''.join(line) for line in lines])
        print(boxes)


class Game:
    """
    A class to represent the Tic Tac Toe Game

    """

    def __init__(self: object) -> object:
        """
        Constructs all necessary attributes of Game object

        """
        self.current_player = 'X'

    def switch_player(self: object) -> None:
        """
        Toggles the value of current player

        Values options are X and O

        """
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

    def get_box_position(self: object) -> int:
        """
        Asks the input position from player
        Check if the position is valid and return its value if valid

        """
        while True:
            print(f'\n Player-{self.current_player}, Enter your position: ')
            try:
                position = int(input('\t>>>> '))
            except ValueError:
                print('\n Position not valid, Please Try Again!')
            else:
                if valid_grid_position(position):
                    pass
                else:
                    print('\n Position not valid, Please Try Again!')
                return position

    def play(self: object) -> None:
        """
        Main Game logic
         - Gets the input position from current player
         - Sets the value of player at the position(if valid)
         - Check if the current player won the game or game ended in draw
         - Else switch the current player and repeat steps

        """
        playing = True
        while playing:
            grid.print_grid()
            position = self.get_box_position()
            grid.set_value(position, self.current_player)

            if player_won():
                grid.print_grid()
                print(
                    f'\nCongratulations Player-{self.current_player}! You WON!!')
                playing = False
            elif game_drawn():
                grid.print_grid()
                print('\nUh Oh! Game Drawn!!')
                playing = False
            else:
                self.switch_player()


def screen_clear() -> None:
    """
    Clears terminal screen window
    """
    if name == 'posix':
        _ = system('clear')
    else:
        _ = system('cls')


def player_won() -> bool:
    """
    Check and return if game has been won by current player

    """
    for i in range(3):
        # Check if all values in single row or column are same and not spaces
        if (len(set(grid.rows[i])) == 1 and ' ' not in grid.rows[i]) or \
           (len(set(grid.cols[i])) == 1 and ' ' not in grid.cols[i]):
            return True

    # Check if all values in a diagonal are same and not spaces
    for i in range(2):
        if len(set(grid.diag[i])) == 1 and ' ' not in grid.diag[i]:
            return True

    return False


def game_drawn() -> bool:
    """
    Check and return if the game has been drawn
    """
    # Game draws if -
    # All 9 boxes of the grid have a value in them
    # None of the player has won
    return len([box for box in grid.grid if box.val != ' ']) == 9


def valid_grid_position(pos) -> bool:
    """
    Check and return if input position is valid

    Parameters
    - - - - - -
    pos: Integer value between 0 and 8 that depicts grid box position

    """

    # Grid Box Position is valid if -
    # The position value is between 0 and 8 (inclusive)
    # The Box value at the position is spaces
    return pos in range(9) and grid.grid[pos].val == ' '


if __name__ == '__main__':
    grid = Grid()
    game = Game()
    game.play()
