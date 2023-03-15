import random
import os

clear = lambda: os.system('clear')

# create a deck of cards
suits = ('❤️', '♦️', '♣️', '♠️')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')
values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + self.suit


class Deck:
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    def __init__(self, total=100):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('How many chips would you like to bet? '))
        except:
            print('Please enter a number')
        else:
            if chips.bet > chips.total:
                print(f'You do not have enough chips, you have {chips.total} chips')
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing
    while True:
        x = input('Would you like to hit or stand? Enter h or s: ').lower()
        if x == 'h':
            hit(deck, hand)
        elif x == 's':
            print(',You stand, Dealer is playing')
            playing = False
        else:
            print('Please enter h or s only')
            continue
        break


def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" Hidden ")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =", dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =", player.value)


def player_busts(player, dealer, chips):
    print('You bust! Better luck next time')
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print('You win!')
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print('Dealer busts!')
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print('Dealer wins!')
    chips.lose_bet()


def push(player, dealer):
    print('Dealer and Player tie!')


# Set up the game
player_chips = Chips()
while True:
    print('Welcome to Blackjack!')
    # Create and shuffle the deck
    deck = Deck()
    deck.shuffle()
    # Deal two cards to the player and dealer
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    # Ask the player for their bet
    take_bet(player_chips)
    # Show the initial hands
    show_some(player_hand, dealer_hand)
    playing = True
    while playing:
        # Ask the player to hit or stand
        hit_or_stand(deck, player_hand)
        # Show the hands again
        show_some(player_hand, dealer_hand)
        # If player's hand exceeds 21, they bust and lose their bet
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break
    # If player hasn't busted, play the dealer's hand
    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
        # Show all hands
        show_all(player_hand, dealer_hand)
        # Determine the winner
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    # Show the player's remaining chips
    print(f'\nPlayer has {player_chips.total} chips')
    # Ask to play again
    play_again = input('Would you like to play again? Enter y or n: ').lower()
    if play_again == 'y':
        clear()
        continue

    else:
        print('Thanks for playing!')
        break
