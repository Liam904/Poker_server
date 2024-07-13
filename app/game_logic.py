import random

# Define ranks and suits for the deck
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

new_ranks = ["4", "5", "6", "7", "8", "9", "10"]
new_suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

joker = ("joker", "joker")


deck = []
player_hand = []
computer_hand = []
tablecard = []

# Function to create and shuffle a deck of cards
def create_deck():
    global deck
    deck = [(rank, suit) for suit in suits for rank in ranks]
    deck.append(joker)
    random.shuffle(deck)

# Function to deal cards to players
def deal_cards():
    global deck, player_hand, computer_hand, tablecard
    create_deck()
    player_hand = deal_cards_helper(4)
    computer_hand = deal_cards_helper(4)
    tablecard.append(deck.pop())

def deal_cards_helper(num_cards):
    return [deck.pop() for _ in range(num_cards)]

# Function to handle player's move
def player_move(rank, suit):
    global player_hand, tablecard
    play = (rank, suit)

    if play in player_hand and (play[0] == tablecard[-1][0] or play[1] == tablecard[-1][1]):
        tablecard.append(play)
        player_hand.remove(play)
        if play[0] == "A":
            pass
        elif play[0] in ["2", "3"]:

            pass
        elif play[0] in ["K", "J"]:
            
            pass
        elif play[0] in ["8", "Q"]:
        
            pass
        return True
    else:
        return False
