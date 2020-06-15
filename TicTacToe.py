from os import name, system


class Box:
    def __init__(self, pos, val):
        self.pos = pos
        self.val = val

    @property
    def posLines(self):
        # Display Grid Positions 
        if self.pos == 0:
            return [(' ' * 3 + "|"), (f'{self.pos:^3}' + '|'), ('-' * 3 + '┘'), ]
        elif self.pos == 1:
            return [(' ' * 3), (f'{self.pos:^3}'), ('-' * 3), ]
        elif self.pos == 2:
            return [('|' + ' ' * 3), ('|' + f'{self.pos:^3}'), ('└' + '-' * 3), ]
        elif self.pos == 3:
            return [(' ' * 3 + '|'), (f'{self.pos:^3}' + '|'), (' ' * 3 + '|'), ]
        elif self.pos == 4:
            return [(' ' * 3), (f'{self.pos:^3}'), (' ' * 3)]
        elif self.pos == 5:
            return [('|' + ' ' * 3), ('|' + f'{self.pos:^3}'), ('|' + ' ' * 3), ]
        elif self.pos == 6:
            return [('-' * 3 + '┐'), (f'{self.pos:^3}' + '|'), (' ' * 3 + '|'), ]
        elif self.pos == 7:
            return [('-' * 3), (f'{self.pos:^3}'), (' ' * 3), ]
        else:
            return [('┌' + '-' * 3), ('|' + f'{self.pos:^3}'), ('|' + ' ' * 3), ]

    @property
    def valLines(self):
        # Display Grid values
        if self.pos == 0:
            return [(' ' * 3 + "|"), (f'{self.val:^3}' + '|'), ('-' * 3 + '┘'), ]
        elif self.pos == 1:
            return [(' ' * 3), (f'{self.val:^3}'), ('-' * 3), ]
        elif self.pos == 2:
            return [('|' + ' ' * 3), ('|' + f'{self.val:^3}'), ('└' + '-' * 3), ]
        elif self.pos == 3:
            return [(' ' * 3 + '|'), (f'{self.val:^3}' + '|'), (' ' * 3 + '|'), ]
        elif self.pos == 4:
            return [(' ' * 3), (f'{self.val:^3}'), (' ' * 3)]
        elif self.pos == 5:
            return [('|' + ' ' * 3), ('|' + f'{self.val:^3}'), ('|' + ' ' * 3), ]
        elif self.pos == 6:
            return [('-' * 3 + '┐'), (f'{self.val:^3}' + '|'), (' ' * 3 + '|'), ]
        elif self.pos == 7:
            return [('-' * 3), (f'{self.val:^3}'), (' ' * 3), ]
        else:
            return [('┌' + '-' * 3), ('|' + f'{self.val:^3}'), ('|' + ' ' * 3), ]


class Grid:
    def __init__(self):
        self.grid = [Box(row * 3 + col, ' ')
                     for row in range(3)
                     for col in range(3)]
        self.setRowColDiag()

    def setRowColDiag(self):
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

    def setValue(self, pos, val):
        self.grid[pos].val = val
        self.setRowColDiag()

    def printGrid(self):
        screen_clear()
        print('\n\t\tTIC-TAC-TOE\t\t Positions\n')

        lines = [[] for i in range(9)]
        for line in lines:
            line.append('\t\t')

        for box in self.grid:
            index = box.pos // 3 * 3
            for line in box.valLines:
                lines[index].append(str(line))
                index += 1

        for line in lines:
            line.append('\t\t')

        for box in self.grid:
            index = box.pos // 3 * 3
            for line in box.posLines:
                lines[index].append(str(line))
                index += 1

        boxes = '\n'.join([''.join(line) for line in lines])
        print(boxes)


class Game:
    def __init__(self):
        self.currentPlayer = 'X'

    def switchPlayer(self):
        if self.currentPlayer == 'X':
            self.currentPlayer = 'O'
        else:
            self.currentPlayer = 'X'

    def playerWon(self):
        for i in range(3):
            if len(set(grid.rows[i])) == 1 and ' ' not in grid.rows[i]:
                return True
            elif len(set(grid.cols[i])) == 1 and ' ' not in grid.cols[i]:
                return True

        for i in range(2):
            if len(set(grid.diag[i])) == 1 and ' ' not in grid.diag[i]:
                return True

        return False

    def gameDrawn(self):
        return len([box for box in grid.grid if box.val != ' ']) == 9

    def validPosition(self, pos):
        return pos in range(9) and grid.grid[pos].val == ' '

    def getPosition(self):
        while True:
            print(f'\n Player-{self.currentPlayer}, Enter your position: ')
            try:
                position = int(input('\t>>>> '))
            except:
                print('\n Position not valid, Please Try Again!')
            else:
                if self.validPosition(position):
                    return position
                else:
                    print('\n Position not valid, Please Try Again!')

    def play(self):
        playing = True
        while playing:
            grid.printGrid()
            position = self.getPosition()
            grid.setValue(position, self.currentPlayer)

            if self.playerWon():
                grid.printGrid()
                print(
                    f'\nCongratulations Player-{self.currentPlayer}! You WON!!')
                playing = False
            elif self.gameDrawn():
                grid.printGrid()
                print(f'\nUh Oh! Game Drawn!!')
                playing = False
            else:
                self.switchPlayer()


def screen_clear():
    if name == 'posix':
        _ = system('clear')
    else:
        _ = system('cls')


if __name__ == '__main__':
    grid = Grid()
    game = Game()
    game.play()
