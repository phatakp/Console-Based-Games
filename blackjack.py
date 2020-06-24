"""
A Multiplayer Black Jack game which also shows current status of table on Command Prompt.

Steps to Play:

1. Add Players (Just need names) - Leave Blank to stop adding
2. Every Player will be alloted $5000 and standard bet of $500.
3. Two cards are dealt to each player and dealer
4. Each player is asked for Hit or Stand
5. Player can split the bet if initial two cards are of same rank.
6. Player can double the bet if initial two cards have combined value of 8, 9 or 10.
7. Bets are settled once, each player has got their chance to play.
"""

from random import shuffle
from os import name, system
from sys import exit
from time import sleep


class Card:
    """
    A class to represent individual card in a deck
    """
    card_values = {'A': 11, 'K': 10, 'Q': 10, 'J': 10}

    def __init__(self: object, suit: str, rank: int) -> object:
        """
        Constructs all necessary attributes of Card object

        Parameters
        - - - - - -
        suit: str value in ('♣', '♠', '♥', '♦')
            Suit of the card
        rank: int value in (2 to 10 or 'A', 'K', 'Q', 'J')
            Rank of the card
        """
        self.suit = suit
        self.rank = rank
        self.points = Card.card_values.get(rank, rank)
        self.back_side = False  # Will be used to hide the card

    @property
    def lines(self: object) -> list:
        """
        Returns a list of lines that generate a card for print

        """
        if self.back_side:
            # This will be hidden card face
            card_print = [
                ('┌' + '-' * 5 + '┐'),              # Line0
                ('|' + '░' * 5 + '|'),              # Line1
                ('|' + '░' * 5 + '|'),              # Line2
                ('|' + '░' * 5 + '|'),              # Line3
                ('|' + '░' * 5 + '|'),              # Line4
                ('|' + '░' * 5 + '|'),              # Line5
                ('└' + '-' * 5 + '┘'),              # Line6
            ]
        else:
            # This will be open card face
            card_print = [
                ('┌' + '-' * 5 + '┐'),              # Line0
                ('|' + f'{self.rank:<5}' + '|'),    # Line1
                ('|' + ' ' * 5 + '|'),              # Line2
                ('|' + f'{self.suit:^5}' + '|'),    # Line3
                ('|' + ' ' * 5 + '|'),              # Line4
                ('|' + f'{self.rank:>5}' + '|'),    # Line5
                ('└' + '-' * 5 + '┘'),              # Line6
            ]
        return card_print

    def __str__(self: object) -> str:
        return ''.join(['(', self.suit, str(self.rank), ',', str(self.points), ')'])


class Deck:
    """
    A class to represent deck of 52 cards
    """
    suits = ('♣', '♠', '♥', '♦')
    ranks = list(range(2, 11)) + list('AKQJ')

    def __init__(self: object) -> object:
        """
        Constructs all attributes required by deck object
        """
        # Create a deck of card objects
        self.cards = [Card(suit, rank)
                      for suit in Deck.suits
                      for rank in Deck.ranks]
        # Shuffle the deck randomly
        shuffle(self.cards)

    def __str__(self: object) -> str:
        return '\n'.join([str(card) for card in self.cards])

    @property
    def shuffle_deck(self: object) -> object:
        """
        Returns a card object from a deck
        """
        return self.cards.pop()


class Player:
    """
    A class to represent player on the table
    """

    def __init__(self: object, first_name: str, dealer: bool = False) -> object:
        """
        Constructs all attributes required by player object

        Parameters
        - - - - - -
        first_name: First name to identify a player
        dealer: Bool to represent whether player is a dealer

        """
        self.name = first_name
        self.dealer = dealer
        self.hand = list()
        self.split_bet = False
        self.is_in_game = True

        # Below values will be converted to list in case of split bet
        self.aces = self.hand_value = self.bet = 0
        self.result = None

        if self.dealer:
            self.chips = 999999
        else:
            self.chips = 5000

    def __str__(self: object) -> str:
        """
        Returns a string representation of player object
        The str value will be used to print the Table status on Command Prompt

        """
        # Current object is Dealer with no cards in hand
        if self.dealer and len(self) == 0:
            text = f"{self.name.upper()} arrived at the table"

        # Current object is Dealer with cards in hand as Black Jack
        elif self.dealer and self.result == 'BLACKJACK':
            text = f"{self.name.upper()} has {self.result}. WON ${int(self.bet):,}"

        # Current object is Dealer and total lost bet
        elif self.dealer and self.bet < 0:
            text = f"{self.name.upper()} has LOST ${int(self.bet)*-1:,}"

        # Current object is Dealer and total won bet
        elif self.dealer and self.result is not None:
            text = f"{self.name.upper()} has WON ${int(self.bet):,}"

        # Current object is Dealer with cards in hand, but game still being played
        elif self.dealer and self.hand[0].back_side and self.result is None:
            text = f"{self.name.upper()} arrived at the table"

        # Current object is Dealer with all players standing
        elif self.dealer and self.result is None:
            text = f"{self.name.upper()} has value ({self.hand_value})"

        # Current object is player with cards in hand and playing split bet
        elif len(self) > 0 and self.split_bet:
            if self.result == [None, None]:
                text = f"{self.name.upper()}{tuple(self.hand_value)} has Split bet for" + \
                    f" (${int(self.bet[0])}, ${int(self.bet[1])})"
            elif self.result == ['BLACKJACK', 'BLACKJACK']:
                text = f"{self.name.upper()} has {self.result[0]} for both Splits." + \
                    f" WON ${int(sum(self.bet)):,}"
            elif self.result[0] == 'BLACKJACK':
                text = f"{self.name.upper()} has {self.result[0]} for Split-1." + \
                    f" WON ${int(self.bet[0]):,}"
            elif self.result[1] == 'BLACKJACK':
                text = f"{self.name.upper()} has {self.result[1]} for Split-2." + \
                    f" WON ${int(self.bet[1]):,}"
            elif not None in self.result and sum(self.bet) >= 0:
                text = f"{self.name.upper()} has {self.result[0]} for Split-1" + \
                    f" and {self.result[1]} for Split-2. WON ${int(sum(self.bet)):,}"
            elif not None in self.result:
                text = f"{self.name.upper()} has {self.result[0]} for Split-1 and" + \
                    f" {self.result[1]} for Split-2. LOST ${int(sum(self.bet)):,}"
            elif self.result[1] is None:
                text = f"{self.name.upper()} has {self.result[0]}" + \
                    f" ${int(self.bet[0]):,} for Split-1"
            else:
                text = f"{self.name.upper()} has {self.result[1]}" + \
                    f" ${int(self.bet[1]):,} for Split-2"

        # Current object is player with card in hand and without split or double bet
        elif len(self) > 0 and self.result is None and self.bet == 500:
            text = f"{self.name.upper()}({self.hand_value})" + \
                f" has bet ${int(self.bet)}"

        # Current object is player with card in hand and double bet
        elif len(self) > 0 and self.result is None:
            text = f"{self.name.upper()}({self.hand_value})" + \
                f" has doubled bet for ${int(self.bet)}"

        # Current object is player with card in hand and BlackJack
        elif len(self) > 0 and self.result == 'BLACKJACK':
            text = f"{self.name.upper()} has {self.result}. WON ${int(self.bet):,}"

        # Current object is player with card in hand and no bets placed
        elif len(self) > 0:
            text = f"{self.name.upper()} has {self.result} ${int(self.bet):,}"

        # Current object is player just arrived at table with no cards in hand
        elif len(self) == 0:
            text = f"{self.name.upper()} is at the table with ${int(self.chips):,}"
        return text

    def __len__(self: object) -> int:
        return len(self.hand)

    @property
    def is_dealer(self: object) -> bool:
        """
        Returns whether a player is a dealer or not

        """
        return self.dealer

    def assign_card(self: object, card: object, split_hand: int = 1) -> None:
        """
        Assigns a card object to player

        Parameters
        - - - - - -
        card: object of class Card, that represents a single card in deck
        split_hand: int paramater, that denotes if player has split bet or not
            Possible values can be 0 or 1 (default is 1)

        """

        # If player is playing split, split_hand value can be 0 or 1
        # Both hands will be separated by ' ' between the cards
        if split_hand == 1:
            # For second split hand, append the card at the end
            self.hand.append(card)
        else:
            # For first split hand, insert the card at beginning
            self.hand.insert(0, card)

        if card.rank == 'A':  # Ace Present
            if self.split_bet:
                self.aces[split_hand] += 1
            else:
                self.aces += 1

        if self.split_bet:
            self.hand_value[split_hand] = self.get_hand_value(split_hand)
        else:
            self.hand_value = self.get_hand_value()

        # Place Player Bet when first cards are dealt
        if len(self) == 1 and not self.is_dealer and not self.split_bet:
            self.place_bet()

    def place_bet(self: object) -> None:
        """
        Method to represent placing a bet by a player
        Bet value will always be 500

        """
        self.bet += 500
        self.chips -= 500

    def get_hand_value(self: object, split_hand: int = 1) -> int:
        """
        Returns total points of cards held by a player as per blackjack rules

        Parameters
        - - - - - -
        split_hand: int paramater, that denotes if player has split bet or not
            Possible values can be 0 or 1 (default is 1)

        """

        if self.split_bet:
            # Separate the hands by ' ' and calculate value
            aces = self.aces[split_hand]
            hand_divider = self.hand.index(' ')
            if split_hand == 0:
                val = sum(map(lambda card: card.points,
                              self.hand[:hand_divider]))
            else:
                val = sum(map(lambda card: card.points,
                              self.hand[hand_divider + 1:]))
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

    def play_split_bet(self: object) -> None:
        """
        Method to split a player hand into two and adjust program variables accordingly

        """
        # For split bet, convert values into list
        self.split_bet = True
        self.chips -= 500
        self.bet = [500, 500]
        self.result = [None, None]
        self.hand.insert(1, ' ')  # Insert a space between two cards
        self.hand_value = [self.hand[0].points, self.hand[2].points]
        self.aces = [1 if self.hand[0].rank == 'A' else 0,
                     1 if self.hand[2].rank == 'A' else 0]

    def print_cards(self: object, message: str = None) -> None:
        """
        Prints the player hand. Cards will be stacked in one line

        Parameters:
        - - - - - -
        message: str paramater that will be printed with cards, if present

        For split bet, two hands will be separated by a tab

        """

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
    """
    A class to represent the BlackJack game

    """

    def __init__(self: object) -> object:
        """
        Constructs all necessary attributes of Game object

        """

        # Start with Dealer as only player
        self.players = [Player('Dealer', dealer=True), ]
        self.dealer = self.players[0]
        self.add_players()

    def __len__(self: object) -> int:
        return len([p for p in self.players if p.is_in_game and not p.is_dealer])

    def add_players(self: object) -> None:
        """
        Method to add player objects to the game

        """

        # Add players until an empty input is encountered.
        # Player name will be asked as input
        while True:
            self.print_table()
            first_name = input('\n\t>>>> New Player Name:  ')
            if first_name > '':
                self.players.append(Player(first_name))
            else:
                break

        # Exit game if no player was added
        if len(self) == 0:
            self.print_table(1)
            print('\n Cannot Continue Game without any Players')
            print('\n EXITING!!!')
            sleep(2)
            exit()

    def print_table(self: object, secs: int = None) -> None:
        """
        Prints the table stats for each player

        Parameters:
        - - - - - -
        secs: int paramater that represent seconds for which the game should execute a delay

        """
        screen_clear(secs)
        print('\t\t', '┌' + '-' * 59 + '┐')
        print('\t\t', f"|{'TABLE STATUS':^59}|")
        print('\t\t', '└' + '-' * 59 + '┘')
        print('\t\t', f"|{'Players on the table:' + str(len(self)):^59}|")
        print('\t\t', '└' + '-' * 59 + '┘')
        for player in self.players:
            print('\t\t', f'|{str(player):^59}|')
            print('\t\t', '└' + '-' * 59 + '┘')

    def play(self: object) -> None:
        """
        Main Game Logic

        1. Two cards are dealt to each player and dealer
        2. Each player is asked for Hit or Stand
        3. Player is dealt a new card, until he chooses to Stand
        4. Player can split the bet if initial two cards are of same rank.
        5. Player can double the bet if initial two cards have combined value of 8, 9 or 10.
        6. Bets are settled once, each player has got their chance to play.

        """
        # Deal two cards to each player and the dealer
        deal_cards()

        # Check if dealer or player got a blackJack
        if not dealer_got_blackjack():
            # Get input from players whether to Hit or Stand
            get_player_moves()
            # Deal cards to player if the total value < 17
            play_dealer_cards()
            # Settle bets based on card values
            settle_bets()


def deal_cards() -> None:
    """
    Deal two cards each (one at a time) to Players and Dealer

    """

    for _ in range(2):
        for player in game.players:
            player.assign_card(deck.shuffle_deck)

    # Hide first card of the Dealer
    game.dealer.hand[0].back_side = True


def dealer_got_blackjack() -> bool:
    """
    Function that returns if dealer got blackJack
    It also checks if any player has blackJack, and settles his/her bet if true

    """
    dealer_has_blackjack = False
    if game.dealer.hand_value == 21:
        # Dealer gets black Jack.
        game.dealer.result = 'BLACKJACK'
        dealer_has_blackjack = True
        game.dealer.hand[0].back_side = False

    # Play ends and bets are settled if dealer has blackJack
    for player in game.players:
        if not player.is_dealer:
            if dealer_has_blackjack:
                game.print_table(1)
                message = '\n' + game.dealer.name.upper() + ' has BLACKJACK!!'
                game.dealer.print_cards(message)
                game.print_table(1)
                if player.hand_value == 21:
                    player.result = 'STANDOFF for'
                    message = '\n' + player.name.upper() + ' also has BLACKJACK!!'
                    player.print_cards(message)
                else:
                    player.result = 'LOST'
                    game.dealer.result = 'WON'
                    game.dealer.bet += player.bet
                    message = '\nSorry' + player.name.upper() + '! You Lost!!'
                    player.print_cards(message)
            else:
                if player.hand_value == 21:
                    player.bet *= 1.5
                    game.dealer.bet -= player.bet
                    player.result = 'BLACKJACK'
                    game.dealer.result = 'LOST'
                    message = '\nCongratulations' + player.name.upper() + '! You got a BLACKJACK!!'
                    player.print_cards(message)
                    player.is_in_game = False

    return dealer_has_blackjack


def get_player_moves() -> None:
    """
    Gets inputs about their move (Hit or Stand) from each player
    It also checks if player is eligible for Split or Double, according to BlackJack rules

    """

    for player in game.players:
        # Get Hit or Stand from each player
        # Also check for Split or Double bets if they are eligible
        if player.is_in_game and not player.is_dealer:
            game.print_table(1)
            message = '\n' + game.dealer.name.upper() + ' Cards'
            game.dealer.print_cards(message)
            message = '\n' + player.name.upper() + ' Cards'
            player.print_cards(message)

            if eligible_for_split(player):
                ask_for_split_bet(player)
            elif eligible_for_double(player):
                ask_for_double_bet(player)

            if player.split_bet:
                for split_hand in range(2):
                    player_hit_or_stand(player, index=split_hand)
            else:
                player_hit_or_stand(player)


def play_dealer_cards() -> None:
    """
    Function that deals cards to Dealer as long the total card value is less or equal to 17
    In accordance to BlackJack rules.

    If total card value exceeds 21, dealer is termed BUSTED!!!

    """
    game.dealer.hand[0].back_side = False
    if len(game) > 0:
        while game.dealer.hand_value < 17:
            # Deal cards to dealer, when the value < 17
            game.print_table(1)
            message = '\nDealing Cards to ' + game.dealer.name.upper()
            game.dealer.print_cards(message)
            game.dealer.assign_card(deck.shuffle_deck)

    game.print_table(1)
    # Check if dealer is BUSTED
    if game.dealer.hand_value > 21:
        game.dealer.is_in_game = False
        game.dealer.result = 'BUSTED'
        message = '\nYay!!' + game.dealer.name.upper() + ' is BUSTED!!'
        game.dealer.print_cards(message)


def settle_bets() -> None:
    """
    Function that settles bets for every player still in game.
    This is after cards are dealt to every player and dealer.

    """
    for player in game.players:
        if player.is_in_game and not player.is_dealer:
            if not game.dealer.is_in_game:
                # Dealer is already BUSTED.
                # Pay up each player that is still in game
                game.print_table(1)
                message = '\nFinal Dealer Cards'
                game.dealer.print_cards(message)
                if player.split_bet:
                    for index, val in enumerate(player.hand_value):
                        if val <= 21:
                            bet_won_by_player(player, index)
                else:
                    bet_won_by_player(player)
            elif player.split_bet:
                for index, val in enumerate(player.hand_value):
                    if game.dealer.hand_value > player.hand_value[index]:
                        bet_lost_by_player(player, index)
                    elif game.dealer.hand_value < player.hand_value[index] <= 21:
                        bet_won_by_player(player, index)
                    else:
                        bet_standoff_with_dealer(player, index)
            elif game.dealer.hand_value > player.hand_value:
                bet_lost_by_player(player)
            elif game.dealer.hand_value < player.hand_value:
                bet_won_by_player(player)
            else:
                bet_standoff_with_dealer(player)


def bet_won_by_player(player: object, index: int = None) -> None:
    """
    Function that settles bet for player that won

    Parameters:
    - - - - - - -
    player: Parameter that denotes object of Player class
    index: int Parameter (only for split bet). Denotes the hand for which player won

    """
    if index is not None:
        # Split bet
        game.dealer.bet -= player.bet[index]
        player.result[index] = 'WON'
        game.dealer.result = 'LOST'
        game.print_table(1)
        message = '\nFinal Dealer Cards'
        game.dealer.print_cards(message)
        message = '\nCongratulations!!' + \
            player.name.upper() + \
            f' You WON for Split: {index+1}!!'
    else:
        game.dealer.bet -= player.bet
        player.result = 'WON'
        game.dealer.result = 'LOST'
        game.print_table(1)
        message = '\nFinal Dealer Cards'
        game.dealer.print_cards(message)
        message = '\nCongratulations!!' + \
            player.name.upper() + \
            ' You WON!!'
    player.print_cards(message)


def bet_lost_by_player(player: object, index: int = None) -> None:
    """
    Function that settles bet for player that lost

    Parameters:
    - - - - - - -
    player: Parameter that denotes object of Player class
    index: int Parameter (only for split bet). Denotes the hand for which player lost

    """
    if index is not None:
        # Split bet
        player.result[index] = 'LOST'
        game.dealer.result = 'WON'
        game.dealer.bet += player.bet[index]
        game.print_table(1)
        message = '\nFinal Dealer Cards'
        game.dealer.print_cards(message)
        message = '\nSorry ' + player.name.upper() + \
            f' You LOST for Split:{index+1}!!'
    else:
        player.result = 'LOST'
        game.dealer.result = 'WON'
        game.dealer.bet += player.bet
        game.print_table(1)
        message = '\nFinal Dealer Cards'
        game.dealer.print_cards(message)
        message = '\nSorry ' + player.name.upper() + \
            ' You LOST!!'
    player.print_cards(message)


def bet_standoff_with_dealer(player: object, index: int = None) -> None:
    """
    Function that settles bet for player that has standoff with dealer

    Parameters:
    - - - - - - -
    player: Parameter that denotes object of Player class
    index: int Parameter (only for split bet). Denotes the hand for which player has standoff

    """
    if index is not None:
        # Split bet
        player.result[index] = 'STANDOFF for'
        game.dealer.result = 'STANDOFF'
        game.print_table(1)
        message = '\nFinal Dealer Cards'
        game.dealer.print_cards(message)
        message = '\nUh Oh!!' + player.name.upper() + \
            f' You have STANDOFF with DEALER for Split:{index+1}!!'
    else:
        player.result = 'STANDOFF for'
        game.dealer.result = 'STANDOFF'
        game.print_table(1)
        message = '\nFinal Dealer Cards'
        game.dealer.print_cards(message)
        message = '\nUh Oh!!' + player.name.upper() + \
            ' You have STANDOFF with DEALER!!'
    player.print_cards(message)


def bet_busted_for_player(player: object, index: int = None) -> None:
    """
    Function that settles bet for player that busted

    Parameters:
    - - - - - - -
    player: Parameter that denotes object of Player class
    index: int Parameter (only for split bet). Denotes the hand for which player busted

    """
    if index is not None:
        # Split bet
        player.result[index] = 'LOST'
        game.dealer.result = 'WON'
        game.dealer.bet += player.bet[index]
        print('\nSorry', player.name.upper(),
              f'! You are BUSTED!! for Split: {index + 1}')
        if not None in player.result:
            player.is_in_game = False
            sleep(3)
    else:
        player.result = 'LOST'
        game.dealer.result = 'WON'
        game.dealer.bet += player.bet
        print('\nSorry', player.name.upper(),
              '! You are BUSTED!!')
        player.is_in_game = False
        sleep(3)


def eligible_for_split(player: object) -> bool:
    """
    Function that returns if a player is eligible for split bet.
    i.e. Two initial cards of the player are of same rank

    Parameters:
    - - - - - - -
    player: Parameter that denotes object of Player class

    """
    return len(player.hand) == 2 and player.hand[0].rank == player.hand[1].rank


def ask_for_split_bet(player: object) -> None:
    """
    Function that asks the player is he/she wants to split bet, when eligible

    Parameters:
    - - - - - - -
    player: Parameter that denotes object of Player class

    """
    while True:
        print('\n\t', player.name.upper(),
              '>>> Do you want to Split (Y or N): ')
        move = input()
        if move.lower() not in ('y', 'n'):
            print('\nInvalid Input. Only enter Y or N')
        else:
            break

    if move.lower() == 'y':
        player.play_split_bet()
        game.print_table(1)
        message = '\n' + game.dealer.name.upper() + ' Cards'
        game.dealer.print_cards(message)
        message = '\n' + player.name.upper() + ' Cards'
        player.print_cards(message)


def eligible_for_double(player: object) -> bool:
    """
    Function that returns if the player is eligible for Double bet
    i.e. The initial two cards of the player has total value in 8, 9 or 10

    Parameters:
    - - - - - - -
    player: Parameter that denotes object of Player class

    """
    return len(player.hand) == 2 and player.hand_value in (8, 9, 10)


def ask_for_double_bet(player: object) -> None:
    """
    Function that asks the player if he wants to play double bet, when eligible

    Parameters:
    - - - - - - -
    player: Parameter that denotes object of Player class

    """
    while True:
        print('\n\t', player.name.upper(),
              '>>> Do you want to Double (Y or N): ')
        move = input()
        if move.lower() not in ('y', 'n'):
            print('\nInvalid Input. Only enter Y or N')
        else:
            break

    if move.lower() == 'y':
        player.place_bet()
        game.print_table(1)
        message = '\n' + game.dealer.name.upper() + ' Cards'
        game.dealer.print_cards(message)
        message = '\n' + player.name.upper() + ' Cards'
        player.print_cards(message)


def player_hit_or_stand(player: object, index: int = None) -> None:
    """
    Function that ask the player for his/her move (Hit or Stand)

    Parameters:
    - - - - - - -
    player: Parameter that denotes object of Player class
    index: int Parameter (only for split bet). Denotes the hand for which player is playing

    """
    if player.split_bet:
        print(f'\n ***** PLAYING SPLIT BET: {index+1} *****')
    while True:
        print('\n\t', player.name.upper(),
              '>>> Do you want to Hit or Stand (H or S): ')
        move = input()
        if move.lower() == 'h':
            if not deal_card_to_player(player, index):
                break
        elif move.lower() == 's':
            break
        else:
            print('\nInvalid Input. Only enter H or S')


def deal_card_to_player(player: object, index: int) -> bool:
    """
    Function that deals new card player when he selects for Hit
    Returns False if player is busted and no longer in game

    Parameters:
    - - - - - - -
    player: Parameter that denotes object of Player class
    index: int Parameter (only for split bet). Denotes the hand for which player is playing

    """
    if index is None:
        index = 1
    player.assign_card(deck.shuffle_deck, split_hand=index)
    game.print_table()
    message = '\n' + game.dealer.name.upper() + ' Cards'
    game.dealer.print_cards(message)
    message = '\n' + player.name.upper() + ' Cards'
    player.print_cards(message)

    if player.split_bet:
        if player.hand_value[index] > 21:
            bet_busted_for_player(player, index)
            return False
    else:
        if player.hand_value > 21:
            bet_busted_for_player(player)
            return False

    return True


def screen_clear(sec: int = None) -> None:
    """
    Clears terminal screen window

    Parameters:
    - - - - - -
    sec: int Parameter when present, the game is delayed by that many seconds

    """
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
