'''Play Black Jack against an AI dealer!'''
# Author: Mitch Gates

import sys
from random import shuffle
from prettytable import PrettyTable
class BlackJack():
    '''BlackJack class object that the game is played within'''

    def __init__(self, num_decks=1):
        self.currency = 100
        self.minimum_bet = 5
        self.suits = {
            "hearts": u"♥",
            "spades": u"♠",
            "diamonds": u"♦",
            "clubs": u"♣"
        }
        self.cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.decks = num_decks
        self.deck = self.__build_deck(self.decks)
        self.player_cards = []
        self.dealer_cards = []
        self.player_sum = 0
        self.dealer_sum = 0
        self.bet = 0
        self.force_shuffle = int(len(self.deck) / 4)


    def play(self):
        '''The main game, this should be called to play BlackJack'''
        while self.currency > 0:
            try:
                self.__reset()
                self.__place_bet()
                self.__deal_cards(2)
                self.__deal_cards(2, dealer=True)
                if self.__sum_cards(self.dealer_cards) != 21:
                    self.__player_actions(self.player_cards)
                if self.__sum_cards(self.player_cards) <= 21 and self.__sum_cards(self.dealer_cards) != 21:
                    self.__dealer_actions()
                self.__pay_winner()
            except KeyboardInterrupt:
                print('Thanks for playing Black Jack!')
                sys.exit()


    def __reset(self):
        '''__resets the player and dealer hands between rounds. Shuffles the deck when necessary.'''
        if len(self.deck) <= self.force_shuffle:
            print('Shuffling Deck')
            self.deck = self.__build_deck(self.decks)

        self.player_cards = []
        self.dealer_cards = []
        self.player_sum = 0
        self.dealer_sum = 0
        self.bet = 0


    def __build_deck(self, decks):
        '''Builds and shuffles a complete deck consisting of the number of decks specified during init'''
        deck = []
        for i in range(decks):
            for card in self.cards:
                for suit in self.suits:
                    deck.append('{} {}'.format(card, suit))
        shuffle(deck)
        return deck


    def __deal_cards(self, num_cards, dealer=False):
        '''Deals the specified number of cards. The default is to deal the cards to the player.

        Args:
            num_cards (str): the number of cards to deal

        Optional:
            dealer (bool): deal to dealer if True
        '''
        if dealer:
            for i in range(num_cards):
                self.dealer_cards.append(self.deck[i])
        else:
            for i in range(num_cards):
                self.player_cards.append(self.deck[i])
        del self.deck[:num_cards]


    def __render_cards(self, cards, dealer=False):
        '''Renders the cards to ascii image. Dealer will have one card face down. Player will have both cards face up.

        Args:
            cards (list): The cards to be rendered

        Optional:
            dealer (bool): If true we hide the first card
        '''
        a = str()
        b = str()
        c = str()
        d = str()
        e = str()
        for card in cards:
            if dealer:
                cardValue = ' '
                cardSuit = ' '
                dealer = False
            else:
                cardValue, cardSuit = card.split()
                cardSuit = self.suits[cardSuit]

            if cardValue != '10':
                cardValue = ' {}'.format(cardValue)

            a += ' -----   '
            b += '|{0}   {0}|  '.format(cardSuit)
            c += '| {}  |  '.format(cardValue)
            d += '|{0}   {0}|  '.format(cardSuit)
            e += ' -----   '

        return '\n'.join([a, b, c, d, e])


    def __display_cards(self, hide_dealer=True):
        '''Displayes the rendered cards and sum of cards using PrettyTable.

        Optional:
            hide_dealer (bool): Hide the dealer's card sum if True
        '''
        x = PrettyTable()
        headers = ['Player Cards', 'Dealer Cards']
        dealer_cards = self.__render_cards(self.dealer_cards, dealer=hide_dealer)
        player_cards = self.__render_cards(self.player_cards)
        player_sum = self.__sum_cards(self.player_cards)
        dealer_sum = '' if hide_dealer else self.__sum_cards(self.dealer_cards)
        x.field_names = headers
        x.add_row([player_cards, dealer_cards])
        x.add_row([player_sum, dealer_sum])
        print(x)

    def __sum_cards(self, cards):
        '''Takes a list of cards and returns the sum of the cards. Ace will use 1 or 11 correctly.

        Args:
            cards (list): A list of cards to sum
        '''
        total = 0
        ace = False
        for card in cards:
            cardValue = card.split()[0]
            if cardValue == 'A':
                total += 1
                ace = True
            elif cardValue == 'J' or cardValue == 'Q' or cardValue == 'K':
                total += 10
            else:
                total += int(cardValue)
        if ace and total + 10 < 22:
            total += 10
        return total


    def __place_bet(self):
        '''Prompts the player for a bet. Bets are required to play!'''
        bet = 0
        while True:
            try:
                bet = input('Place a bet ({} min, {} max, q to quit): '.format(self.minimum_bet, self.currency))
                if bet.upper() == 'Q':
                    raise KeyboardInterrupt
                bet = int(bet)
            except ValueError:
                print('Invalid bet, try again.')
                continue

            if bet < self.minimum_bet or bet > self.currency:
                print('Invalid bet, try again.')
            else:
                self.bet = bet
                break


    def __player_actions(self, cards):
        '''Prompts the player for actions to take.

        Args:
            Cards (list): A list of of the player's cards
        '''
        actions = {
            'Hit': 'H',
            'Stay': 'S',
            'Double Down': 'D',
            'Split': 'Y',
            'Quit': 'Q'
        }

        while True:
            current_actions = actions.copy()
            if 'Double Down' in actions:
                del actions['Double Down']

            card_values = []
            for card in cards:
                card_values.append(card.split()[0])

            if self.__sum_cards(self.player_cards) > 21:
                break
            elif self.__sum_cards(self.player_cards) == 21:
                break
            else:
                self.__display_cards()

            if not card_values.count(card_values[0]) == len(card_values):
                del current_actions['Split']

            action = input('Choose an action: {}'.format(current_actions))

            if action.upper() == 'H':
                self.__deal_cards(1)
            elif action.upper() == 'S':
                break
            elif action.upper() == 'D':
                self.bet += self.bet
                print('Doubling down! Your current bet is now {}.'.format(self.bet))
                self.__deal_cards(1)
            elif action.upper() == 'Q':
                raise KeyboardInterrupt()


    def __dealer_actions(self):
        '''Automates through the dealer's actions. Hits on 16 or lower, stays on 17 or higher.'''
        # if self.__sum_cards(self.dealer_cards) > self.__sum_cards(self.player_cards):
            # self.__display_cards(hide_dealer=False)
            # return

        while True:
            # self.__display_cards(hide_dealer=False)

            if self.__sum_cards(self.dealer_cards) == 21:
                break
            elif self.__sum_cards(self.dealer_cards) <= 16:
                self.__deal_cards(1, dealer=True)
            elif self.__sum_cards(self.dealer_cards) > 21:
                break
            else:
                break


    def __pay_winner(self):
        '''Pays out to the winner. Currency is adjusted.'''
        self.__display_cards(hide_dealer=False)
        player_sum = self.__sum_cards(self.player_cards)
        dealer_sum = self.__sum_cards(self.dealer_cards)
        while True:
            if player_sum > 21:
                print('You busted!')
                print('You pay the dealer {}.'.format(self.bet))
                self.currency -= self.bet
                break

            if dealer_sum > 21:
                print('Dealer busted!')
                print('Dealer pays you {}.'.format(self.bet))
                self.currency += self.bet
                break

            if player_sum == 21 and dealer_sum != 21 and len(self.player_cards) == 2:
                print('You got a blackjack!')
                print('Dealer pays you {}'.format(self.bet * 1.5))
                self.currency += self.bet * 1.5
                break

            if dealer_sum == 21 and len(self.dealer_cards) == 2:
                print('Dealer got a blackjack!')
                print('You pay the dealer {}'.format(self.bet))
                self.currency -= self.bet
                break

            if self.__sum_cards(self.player_cards) == self.__sum_cards(self.dealer_cards):
                print('Push - keep your bet.')
                break

            if self.__sum_cards(self.player_cards) < self.__sum_cards(self.dealer_cards):
                print('You pay the dealer {}.'.format(self.bet))
                self.currency -= self.bet
                break

            if self.__sum_cards(self.player_cards) > self.__sum_cards(self.dealer_cards):
                print('Dealer pays you {}.'.format(self.bet))
                self.currency += self.bet
                break
        print('You now have {} currency.'.format(self.currency))


if __name__ == '__main__':
    bj = BlackJack(num_decks=1)
    bj.play()
