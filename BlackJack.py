'''Play Blackjack against an AI dealer!'''
# Author: Mitch Gates

import sys
from random import shuffle
from prettytable import PrettyTable
class Blackjack():
    '''Blackjack class object that the game is played within'''

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
        self.player_cards = [ [] ]
        self.dealer_cards = [ [] ]
        self.player_sum = 0
        self.dealer_sum = 0
        self.bet = 0
        self.force_shuffle = int(len(self.deck) / 4)
        self.blackjacks = []


    def __reset(self):
        '''__resets the player and dealer hands between rounds. Shuffles the deck when necessary.'''
        if len(self.deck) <= self.force_shuffle:
            print('Only {} cards remain in the deck. Shuffling deck.'.format(len(self.deck)))
            self.deck = self.__build_deck(self.decks)

        self.player_cards = [ [] ]
        self.dealer_cards = [ [] ]
        self.player_sum = 0
        self.dealer_sum = 0
        self.bet = 0


    def play(self):
        '''The main game, this should be called to play BlackJack'''
        while self.currency > self.minimum_bet:
            try:
                self.__reset()
                self.__place_bet()
                self.__deal_cards(2)
                self.__deal_cards(2, dealer=True)
                self.__player_actions(self.player_cards)
                self.__dealer_actions()
                self.__pay_winner()
            except KeyboardInterrupt:
                break
        self.__exit()


    def __exit(self):
        print('Thanks for playing Blackjack! You walked away with {} currency.'.format(self.currency))
        sys.exit()


    def __build_deck(self, decks):
        '''Builds and shuffles a complete deck consisting of the number of decks specified during init'''
        deck = []
        for i in range(decks):
            for card in self.cards:
                for suit in self.suits:
                    deck.append('{} {}'.format(card, suit))
        shuffle(deck)
        return deck


    def __deal_cards(self, num_cards, card_set=0, dealer=False):
        '''Deals the specified number of cards. The default is to deal the cards to the player.

        Args:
            num_cards (str): the number of cards to deal

        Optional:
            card_set (int): the card set to deal a card to (could have multiple if a player splits)
            dealer (bool): deal to dealer if True
        '''
        if dealer:
            for i in range(num_cards):
                self.dealer_cards[0].append(self.deck[i])
        else:
            for i in range(num_cards):
                self.player_cards[card_set].append(self.deck[i])
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


    def __display_cards(self, cards, hide_dealer=True):
        '''Displayes the rendered cards and sum of cards using PrettyTable.

        Optional:
            hide_dealer (bool): Hide the dealer's card sum if True
        '''
        x = PrettyTable()
        headers = ['Player Cards', 'Dealer Cards']
        dealer_cards = self.__render_cards(self.dealer_cards[0], dealer=hide_dealer)
        player_cards = self.__render_cards(cards)
        player_sum = self.__sum_cards(cards)
        dealer_sum = '' if hide_dealer else self.__sum_cards(self.dealer_cards[0])
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
                bet = input('Place a bet <{} min, {} max, q to quit>: '.format(self.minimum_bet, self.currency))
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
        actions = ['(H)it', '(S)tay', '(D)ouble Down', 'Spli(T)', '(Q)uit']
        for i, card_set in enumerate(cards):
            current_actions = actions.copy()
            if '(D)ouble Down' in actions:
                actions.remove('(D)ouble Down')
            while True:
                card_values = []
                for card in card_set:
                    card_values.append(card.split()[0])

                if self.__sum_cards(self.dealer_cards[0]) == 21 and len(self.dealer_cards[0]) == 2:
                    # dealer got a blackjack
                    break
                if self.__sum_cards(self.player_cards[i]) > 21:
                    # player buested
                    break
                elif self.__sum_cards(self.player_cards[i]) == 21 and len(self.player_cards[i]) == 2:
                    # player got a blackjack
                    self.blackjacks.append(self.player_cards[i])
                    break
                else:
                    self.__display_cards(self.player_cards[i])

                if not card_values.count(card_values[0]) == 2 and 'Spli(T)' in current_actions:
                    current_actions.remove('Spli(T)')

                # Prompt the user for an action
                action = input('Choose an action <{}>:'.format(', '.join(current_actions)))

                # Perform action based on user input
                if action.upper() == 'H':
                    self.__deal_cards(1, card_set=i)
                elif action.upper() == 'S':
                    break
                elif action.upper() == 'D':
                    if self.currency - (self.bet * 2) >= 0:
                        # Double our bet if we have the currency
                        self.bet += self.bet
                    else:
                        # Use the remainder of our currency for a double-down
                        self.bet += (self.currency - self.bet)
                    print('Doubling down! Your current bet is now {}.'.format(self.bet))
                    self.__deal_cards(1, card_set=i)
                    break
                elif action.upper() == 'T' and 'Spli(T)' in current_actions:
                    self.bet += self.bet
                    print('Splitting cards! Your current bet is now {}'.format(self.bet))
                    self.__split_cards()
                elif action.upper() == 'Q':
                    raise KeyboardInterrupt()
                else:
                    print('Invalid action. Try again.')


    def __split_cards(self):
        '''Splits the players cards that are matching into new hands.'''
        for i, card_set in enumerate(self.player_cards):
            card_values = []
            for card in card_set:
                card_values.append(card[0])
            if len(card_set) > 1 and card_values.count(card_values[0]) > 1:
                self.player_cards.append([self.player_cards[i].pop(0)])


    def __dealer_actions(self):
        '''Automates through the dealer's actions. Hits on 16 or lower, stays on 17 or higher.'''
        for i in range(len(self.player_cards)):
            while self.__sum_cards(self.dealer_cards[0]) <= 16:
                if self.player_cards[i] in self.blackjacks:
                    # Player has a blackjack, don't bet this hand
                    break
                elif self.__sum_cards(self.player_cards[i]) > 21:
                    # Player busted
                    break
                elif self.__sum_cards(self.dealer_cards[0]) == 21:
                    # Dealer has 21
                    break
                elif self.__sum_cards(self.dealer_cards[0]) > 21:
                    # Dealer busted
                    break
                else:
                    # Dealer plays
                    self.__deal_cards(1, dealer=True)


    def __pay_winner(self):
        '''Pays out to the winner. Currency is adjusted.'''
        dealer_sum = self.__sum_cards(self.dealer_cards[0])
        for i in range(len(self.player_cards)):
            self.__display_cards(self.player_cards[i], hide_dealer=False)
            player_sum = self.__sum_cards(self.player_cards[i])
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

                if player_sum == 21 and dealer_sum != 21 and len(self.player_cards[i]) == 2:
                    print('You got a blackjack!')
                    print('Dealer pays you {}'.format(self.bet * 1.5))
                    self.currency += self.bet * 1.5
                    break

                if dealer_sum == 21 and len(self.dealer_cards[0]) == 2:
                    print('Dealer got a blackjack!')
                    print('You pay the dealer {}'.format(self.bet))
                    self.currency -= self.bet
                    break

                if player_sum == dealer_sum:
                    print('Push - keep your bet.')
                    break

                if player_sum < dealer_sum:
                    print('You pay the dealer {}.'.format(self.bet))
                    self.currency -= self.bet
                    break

                if player_sum > dealer_sum:
                    print('Dealer pays you {}.'.format(self.bet))
                    self.currency += self.bet
                    break
        print()
        print('You now have {} currency.'.format(self.currency))


if __name__ == '__main__':
    bj = Blackjack(num_decks=1)
    bj.play()
