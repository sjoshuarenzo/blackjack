import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,'Queen':10, 'King':10, 'Ace':11}

playing = True

# Classes

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck:

    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)

                self.deck.append(created_card)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n' + str(card)
        return 'Deck includes:\n' + deck_comp

class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self):
        self.total = 100
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

# Functions

def take_bet(chips):
    while True:
        try:
            bet = int(input(f'You have a total of {chips.total} chips total. Place your bet: '))
        except:
            print("Oops, that's not a valid amount. Try again!")
        else:
            if bet > chips.total:
                print("Not enough chips! Place a lower bet.")
            else:
                chips.bet = bet
                break

def hit(deck,hand):
    hand.add_card(deck.deal())

def hit_or_stand(deck,hand):
    global playing

    while True:
        hitstand = input("Do you want to hit or stand? (y/n)").lower()
        
        if hitstand in ("y","yes"):
            hit(deck,hand)
            break
        elif hitstand in ("n","no"):
            print("Player stops playing. Dealer's turn.")
            playing = False
            break
        else:
            print("I do not understand. Please enter y or n")

def show_some(player,dealer):
    print("The player's cards are:")
    for card in player.cards:
        print(card)
    print(f"The dealer's cards are:\n<Hidden Card>\n{dealer.cards[1]}")

def show_all(player,dealer):
    print("The player's cards are:")
    for card in player.cards:
        print(card)
    print(f"Total value of Player's cards: {player.value}")
    print("The dealer's cards are:")
    for card in dealer.cards:
        print(card)
    print(f"Total value of Dealer's cards: {dealer.value}")

def player_busts(chips):
    print("Player busts. You lose!")
    chips.lose_bet()

def player_wins(chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(chips):
    print("Dealer busts. You win!")
    chips.win_bet()

def dealer_wins(chips):
    print("Dealer wins. You lose!")
    chips.lose_bet()

def push():
    print("Tie")

# Main Game Loop

while True:
    print("Blackjack")
    playing = True
    
    player_hand = Hand()
    dealer_hand = Hand()

    this_deck = Deck()
    this_deck.shuffle()

    for x in range(2):
        player_hand.add_card(this_deck.deal())
        dealer_hand.add_card(this_deck.deal())

    player_hand.adjust_for_ace()
    dealer_hand.adjust_for_ace()

    player_chips = Chips()

    take_bet(player_chips)

    show_some(player_hand,dealer_hand)

    while playing:
        hit_or_stand(this_deck,player_hand)

        player_hand.adjust_for_ace()
        
        show_some(player_hand,dealer_hand)

        if player_hand.value > 21:
            player_busts(player_chips)
            playing = False
            break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            dealer_hand.add_card(this_deck.deal())

            dealer_hand.adjust_for_ace()

        show_all(player_hand,dealer_hand)

        if player_hand.value == dealer_hand.value:
            push()
        elif dealer_hand.value > 21:
            dealer_busts(player_chips)
        elif dealer_hand.value == 21 or dealer_hand.value > player_hand.value:
            dealer_wins(player_chips)
        elif player_hand.value == 21 or player_hand.value > dealer_hand.value:
            player_wins(player_chips)

    print(f"You have a total of {player_chips.total} chips.")

    try:
        play_again = input("Play again? (y/n)").lower()
    except:
        print("I do not understand. Enter y or n.")
    else:
        if play_again in ("n","no"):
            break



