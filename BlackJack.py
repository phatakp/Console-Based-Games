from random import shuffle
from os import name, system
from sys import exit
from time import sleep
from functools import reduce


class Card:
    card_values = {'A': 11, 'K': 10, 'Q': 10, 'J': 10}

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.points = Card.card_values.get(rank, rank)
        self.backSide = False

    @property
    def lines(self):
        if self.backSide:
            # Need to hide the card face
            return [
                ('┌' + '-' * 5 + '┐'),              # Line0
                ('|' + '░' * 5 + '|'),              # Line1
                ('|' + '░' * 5 + '|'),              # Line2
                ('|' + '░' * 5 + '|'),              # Line3
                ('|' + '░' * 5 + '|'),              # Line4
                ('|' + '░' * 5 + '|'),              # Line5
                ('└' + '-' * 5 + '┘'),              # Line6
            ]
        else:
            return [
                ('┌' + '-' * 5 + '┐'),              # Line0
                ('|' + f'{self.rank:<5}' + '|'),    # Line1
                ('|' + ' ' * 5 + '|'),              # Line2
                ('|' + f'{self.suit:^5}' + '|'),    # Line3
                ('|' + ' ' * 5 + '|'),              # Line4
                ('|' + f'{self.rank:>5}' + '|'),    # Line5
                ('└' + '-' * 5 + '┘'),              # Line6
            ]

    def __str__(self):
        return ''.join(['(', self.suit, str(self.rank), ',', str(self.points), ')'])


class Deck:
    suits = ('♣', '♠', '♥', '♦')
    ranks = list(range(2, 11)) + list('AKQJ')

    def __init__(self):
        self.cards = [Card(suit, rank)
                      for suit in Deck.suits
                      for rank in Deck.ranks]
        shuffle(self.cards)

    def __str__(self):
        return '\n'.join([str(card) for card in self.cards])

    @property
    def _shuffle(self):
        return self.cards.pop()


class Player:
    def __init__(self, first_name, dealer=False):
        self.name = first_name
        self.dealer = dealer
        self.hand = list()
        self.split_bet = False
        self.aces = 0
        self.handValue = 0
        self.bet = 0
        self.isInGame = True
        self.result = None

        if self.dealer:
            self.chips = 999999
        else:
            self.chips = 5000

    def __str__(self):
        if self.dealer:
            if len(self) == 0:
                return f"{self.name.upper()} arrived at the table"
            elif self.result:
                if self.result == 'BLACKJACK':
                    return f"{self.name.upper()} has {self.result}. WON ${int(self.bet):,}"
                elif self.bet < 0:
                    return f"{self.name.upper()} has LOST ${int(self.bet)*-1:,}"
                else:
                    return f"{self.name.upper()} has WON ${int(self.bet):,}"
            else:
                if self.hand[0].backSide:
                    return f"{self.name.upper()} arrived at the table"
                else:
                    return f"{self.name.upper()} has value ({self.handValue})"
        else:
            if len(self) > 0:
                if self.split_bet:
                    if self.result == [None, None]:
                        return f"{self.name.upper()}{tuple(self.handValue)} has Split bet for (${int(self.bet[0])}, ${int(self.bet[1])})"
                    elif self.result == ['BLACKJACK', 'BLACKJACK']:
                        return f"{self.name.upper()} has {self.result[0]} for both Splits. WON ${int(sum(self.bet)):,}"
                    elif self.result[0] == 'BLACKJACK':
                        return f"{self.name.upper()} has {self.result[0]} for Split-1. WON ${int(self.bet[0]):,}"
                    elif self.result[1] == 'BLACKJACK':
                        return f"{self.name.upper()} has {self.result[1]} for Split-2. WON ${int(self.bet[1]):,}"
                    elif not None in self.result:
                        if sum(self.bet) >= 0:
                            return f"{self.name.upper()} has {self.result[0]} for Split-1 and {self.result[1]} for Split-2. WON ${int(sum(self.bet)):,}"
                        else:
                            return f"{self.name.upper()} has {self.result[0]} for Split-1 and {self.result[1]} for Split-2. LOST ${int(sum(self.bet)):,}"
                    elif self.result[1] is None:
                        return f"{self.name.upper()} has {self.result[0]} ${int(self.bet[0]):,} for Split-1"
                    else:
                        return f"{self.name.upper()} has {self.result[1]} ${int(self.bet[1]):,} for Split-2"
                else:
                    if self.result is None:
                        if self.bet == 500:
                            return f"{self.name.upper()}({self.handValue}) has bet ${int(self.bet)}"
                        else:
                            return f"{self.name.upper()}({self.handValue}) has doubled bet for ${int(self.bet)}"
                    elif self.result == 'BLACKJACK':
                        return f"{self.name.upper()} has {self.result}. WON ${int(self.bet):,}"
                    else:
                        return f"{self.name.upper()} has {self.result} ${int(self.bet):,}"
            else:
                return f"{self.name.upper()} is at the table with ${int(self.chips):,}"

    def __len__(self):
        return len(self.hand)

    @property
    def isDealer(self):
        return self.dealer

    def assignCard(self, card, splitHand=1):
        # If player is playing split, splitHand value can be 0 or 1
        if splitHand == 1:
            self.hand.append(card)
        else:
            self.hand.insert(0, card)

        if card.rank == 'A':  # Ace Present
            if self.split_bet:
                self.aces[splitHand] += 1
            else:
                self.aces += 1

        if self.split_bet:
            self.handValue[splitHand] = self.getHandValue(splitHand)
        else:
            self.handValue = self.getHandValue()

        # Place Player Bet when first cards are dealt
        if len(self) == 1 and not self.isDealer and not self.split_bet:
            self.placeBet()

    def placeBet(self):
        self.bet += 500
        self.chips -= 500

    def getHandValue(self, splitHand=1):
        if self.split_bet:
            aces = self.aces[splitHand]
            handDivider = self.hand.index(' ')
            if splitHand == 0:
                val = sum(map(lambda card: card.points,
                              self.hand[:handDivider]))
            else:
                val = sum(map(lambda card: card.points,
                              self.hand[handDivider + 1:]))
        else:
            val = sum(map(lambda card: card.points, self.hand))
            aces = self.aces

        while val > 21:
            if aces > 0:
                val -= 10
                aces -= 1
            else:
                break

        return val

    def playSplitBet(self):
        self.split_bet = True
        self.chips -= 500
        self.bet = [500, 500]
        self.result = [None, None]
        self.hand.insert(1, ' ')  # Insert a space between two cards
        self.handValue = [self.hand[0].points, self.hand[2].points]
        self.aces = [1 if self.hand[0].rank == 'A' else 0,
                     1 if self.hand[2].rank == 'A' else 0]

    def printCards(self, message=None):
        # There are seven lines in each card-print
        lines = [[] for i in range(7)]

        for card in self.hand:
            # Insert a tab display for split bet cards
            if card == ' ':
                for i in range(7):
                    lines[i].append('\t')
            else:
                for index, line in enumerate(card.lines):
                    lines[index].append(str(line))

        cards = '\n'.join(['\t'.join(line) for line in lines])

        if message:
            print(message)
        print(cards)


class Game:
    def __init__(self):
        # Start with Dealer as only player
        self.players = [Player('Dealer', dealer=True), ]
        self.dealer = self.players[0]
        self.addPlayers()

    def __len__(self):
        return len([p for p in self.players if p.isInGame and not p.isDealer])

    def addPlayers(self):
        while True:
            self.printTable()
            first_name = input('\n\t>>>> New Player Name:  ')
            if first_name > '':
                self.players.append(Player(first_name))
            else:
                break

        if len(self) == 0:
            self.printTable(1)
            print('\n Cannot Continue Game without any Players')
            print('\n EXITING!!!')
            sleep(2)
            exit()

    def printTable(self, secs=None):
        screen_clear(secs)
        print('\t\t', '┌' + '-' * 59 + '┐')
        print('\t\t', f"|{'TABLE STATUS':^59}|")
        print('\t\t', '└' + '-' * 59 + '┘')
        print('\t\t', f"|{'Players on the table:' + str(len(self)):^59}|")
        print('\t\t', '└' + '-' * 59 + '┘')
        for player in self.players:
            print('\t\t', f'|{str(player):^59}|')
            print('\t\t', '└' + '-' * 59 + '┘')

    def play(self):
        dealCards()
        if not blackJack():
            getPlayerMoves()
            playDealer()
            settleBets()


def dealCards():
    # Deal two cards each (one at a time) to Players and Dealer
    for _ in range(2):
        for player in game.players:
            player.assignCard(deck._shuffle)

    # Hide first card of the Dealer
    game.dealer.hand[0].backSide = True


def blackJack():
    dealer_got_blackJack = False
    if game.dealer.handValue == 21:
        game.dealer.result = 'BLACKJACK'
        dealer_got_blackJack = True
        game.dealer.hand[0].backSide = False

    for player in game.players:
        if not player.isDealer:
            if dealer_got_blackJack:
                game.printTable(1)
                message = '\n' + game.dealer.name.upper() + ' has BLACKJACK!!'
                game.dealer.printCards(message)
                game.printTable(1)
                if player.handValue == 21:
                    player.result = 'STANDOFF for'
                    message = '\n' + player.name.upper() + ' also has BLACKJACK!!'
                    player.printCards(message)
                else:
                    player.result = 'LOST'
                    game.dealer.result = 'WON'
                    game.dealer.bet += player.bet
                    message = '\nSorry' + player.name.upper() + '! You Lost!!'
                    player.printCards(message)
            else:
                if player.handValue == 21:
                    player.bet *= 1.5
                    game.dealer.bet -= player.bet
                    player.result = 'BLACKJACK'
                    game.dealer.result = 'LOST'
                    message = '\nCongratulations' + player.name.upper() + '! You got a BLACKJACK!!'
                    player.printCards(message)
                    player.isInGame = False

    return dealer_got_blackJack


def getPlayerMoves():
    for player in game.players:
        if player.isInGame and not player.isDealer:
            game.printTable(1)
            message = '\n' + game.dealer.name.upper() + ' Cards'
            game.dealer.printCards(message)
            message = '\n' + player.name.upper() + ' Cards'
            player.printCards(message)

            if eligibleForSplit(player):
                askForSplit(player)
            elif eligibleForDouble(player):
                askForDouble(player)

            if player.split_bet:
                for splitHand in range(2):
                    wantToHitorStand(player, index=splitHand)
            else:
                wantToHitorStand(player)


def playDealer():
    game.dealer.hand[0].backSide = False
    if len(game) > 0:
        while game.dealer.handValue < 17:
            game.printTable(1)
            message = '\nDealing Cards to ' + game.dealer.name.upper()
            game.dealer.printCards(message)
            game.dealer.assignCard(deck._shuffle)

    game.printTable(1)
    if game.dealer.handValue > 21:
        game.dealer.isInGame = False
        game.dealer.result = 'BUSTED'
        message = '\nYay!!' + game.dealer.name.upper() + ' is BUSTED!!'
        game.dealer.printCards(message)


def settleBets():
    for player in game.players:
        if player.isInGame and not player.isDealer:
            if not game.dealer.isInGame:
                game.printTable(1)
                message = '\nFinal Dealer Cards'
                game.dealer.printCards(message)
                if player.split_bet:
                    for index, val in enumerate(player.handValue):
                        if val <= 21:
                            betWon(player, index)
                else:
                    betWon(player)
            else:
                if player.split_bet:
                    for index, val in enumerate(player.handValue):
                        if game.dealer.handValue > player.handValue[index]:
                            betLost(player, index)
                        elif game.dealer.handValue < player.handValue[index] <= 21:
                            betWon(player, index)
                        else:
                            betStandoff(player, index)
                else:
                    if game.dealer.handValue > player.handValue:
                        betLost(player)
                    elif game.dealer.handValue < player.handValue:
                        betWon(player)
                    else:
                        betStandoff(player)


def betWon(player, index=None):
    if index is not None:
        game.dealer.bet -= player.bet[index]
        player.result[index] = 'WON'
        game.dealer.result = 'LOST'
        game.printTable(1)
        message = '\nFinal Dealer Cards'
        game.dealer.printCards(message)
        message = '\nCongratulations!!' + \
            player.name.upper() + \
            f' You WON for Split: {index+1}!!'
    else:
        game.dealer.bet -= player.bet
        player.result = 'WON'
        game.dealer.result = 'LOST'
        game.printTable(1)
        message = '\nFinal Dealer Cards'
        game.dealer.printCards(message)
        message = '\nCongratulations!!' + \
            player.name.upper() + \
            f' You WON!!'
    player.printCards(message)


def betLost(player, index=None):
    if index is not None:
        player.result[index] = 'LOST'
        game.dealer.result = 'WON'
        game.dealer.bet += player.bet[index]
        game.printTable(1)
        message = '\nFinal Dealer Cards'
        game.dealer.printCards(message)
        message = '\nSorry ' + player.name.upper() + \
            f' You LOST for Split:{index+1}!!'
    else:
        player.result = 'LOST'
        game.dealer.result = 'WON'
        game.dealer.bet += player.bet
        game.printTable(1)
        message = '\nFinal Dealer Cards'
        game.dealer.printCards(message)
        message = '\nSorry ' + player.name.upper() + \
            f' You LOST!!'
    player.printCards(message)


def betStandoff(player, index=None):
    if index is not None:
        player.result[index] = 'STANDOFF for'
        game.dealer.result = 'STANDOFF'
        game.printTable(1)
        message = '\nFinal Dealer Cards'
        game.dealer.printCards(message)
        message = '\nUh Oh!!' + player.name.upper() + \
            f' You have STANDOFF with DEALER for Split:{index+1}!!'
    else:
        player.result = 'STANDOFF for'
        game.dealer.result = 'STANDOFF'
        game.printTable(1)
        message = '\nFinal Dealer Cards'
        game.dealer.printCards(message)
        message = '\nUh Oh!!' + player.name.upper() + \
            f' You have STANDOFF with DEALER!!'
    player.printCards(message)


def betBusted(player, index=None):
    if index is not None:
        player.result[index] = 'LOST'
        game.dealer.result = 'WON'
        game.dealer.bet += player.bet[index]
        print('\nSorry', player.name.upper(),
              f'! You are BUSTED!! for Split: {index + 1}')
        if not None in player.result:
            player.isInGame = False
            sleep(3)
    else:
        player.result = 'LOST'
        game.dealer.result = 'WON'
        game.dealer.bet += player.bet
        print('\nSorry', player.name.upper(),
              f'! You are BUSTED!!')
        player.isInGame = False
        sleep(3)


def eligibleForSplit(player):
    return len(player.hand) == 2 and player.hand[0].rank == player.hand[1].rank


def askForSplit(player):
    while True:
        print('\n\t', player.name.upper(),
              '>>> Do you want to Split (Y or N): ')
        move = input()
        if move.lower() in ('y', 'n'):
            break
        else:
            print('\nInvalid Input. Only enter Y or N')

    if move.lower() == 'y':
        player.playSplitBet()
        game.printTable(1)
        message = '\n' + game.dealer.name.upper() + ' Cards'
        game.dealer.printCards(message)
        message = '\n' + player.name.upper() + ' Cards'
        player.printCards(message)


def eligibleForDouble(player):
    return len(player.hand) == 2 and player.handValue in (8, 9, 10)


def askForDouble(player):
    while True:
        print('\n\t', player.name.upper(),
              '>>> Do you want to Double (Y or N): ')
        move = input()
        if move.lower() in ('y', 'n'):
            break
        else:
            print('\nInvalid Input. Only enter Y or N')

    if move.lower() == 'y':
        player.placeBet()
        game.printTable(1)
        message = '\n' + game.dealer.name.upper() + ' Cards'
        game.dealer.printCards(message)
        message = '\n' + player.name.upper() + ' Cards'
        player.printCards(message)


def wantToHitorStand(player, index=None):
    if player.split_bet:
        print(f'\n ***** PLAYING SPLIT BET: {index+1} *****')
    while True:
        print('\n\t', player.name.upper(),
              '>>> Do you want to Hit or Stand (H or S): ')
        move = input()
        if move.lower() == 'h':
            if not dealCardToPlayer(player, index):
                break
        elif move.lower() == 's':
            break
        else:
            print('\nInvalid Input. Only enter H or S')


def dealCardToPlayer(player, index):
    if index is None:
        index = 1
    player.assignCard(deck._shuffle, splitHand=index)
    game.printTable()
    message = '\n' + game.dealer.name.upper() + ' Cards'
    game.dealer.printCards(message)
    message = '\n' + player.name.upper() + ' Cards'
    player.printCards(message)

    if player.split_bet:
        if player.handValue[index] > 21:
            betBusted(player, index)
            return False
    else:
        if player.handValue > 21:
            betBusted(player)
            return False

    return True


def screen_clear(sec=None):
    if sec:
        sleep(sec)

    if name == 'posix':
        _ = system('clear')
    else:
        _ = system('cls')


if __name__ == '__main__':

    deck = Deck()
    game = Game()
    game.play()
