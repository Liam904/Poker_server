import random
from app.models import Card, Game, db, Player


class GameEngine:
    def __init__(self):
        self.deck = []
        self.player_hand = []
        self.computer_hand = []
        self.tablecard = []

    def create_deck(self):
        cards = Card.query.all()
      
        if self.deck is not None:
            self.reset_deck()

        for card in cards:
            card_list = (card.rank, card.suit)
            self.deck.append(card_list)
            random.shuffle(self.deck)

        
        return self.deck

    def deal_cards(self):
        if not self.deck:
            return {"Message": "No deck found"}
        
        if self.player_hand  or self.computer_hand is not None:
            self.reset_cards()
            
        for _ in range(4):
            self.player_hand.append(self.deck.pop())
            self.computer_hand.append(self.deck.pop())

        self.tablecard.append(self.deck.pop())
        return {
            "player_hand": self.player_hand,
            "computer_hand": self.computer_hand,
            "table_card": self.tablecard,
        }

    def player_moves(self, rank, suit):
        play = (rank, suit)
        if not self.deck:
            return {"message":"deck is empty"}
        if play in self.player_hand and (
            play[0] == self.tablecard[-1][0] or play[1] == self.tablecard[-1][1]
        ):
            self.tablecard.append(play)
            self.player_hand.remove(play)
            if play[0] in ["2", "3"]:
                penalty_cards = 2 if play[0] == "2" else 3
                for _ in range(penalty_cards):
                    if self.deck:
                        self.computer_hand.append(self.deck.pop())

            if play[0] in ["K", "Q", "J", "8"]:
                self.player_moves()
                self.computer_moves()
        if play[0]=="pick":
            self.player_hand.append(self.deck.pop())

        else:
            return {"message": "Invalid move"}
        return {
            "player_hand": self.player_hand,
            "computer_hand": self.computer_hand,
            "table_card": self.tablecard,
        }

    def computer_moves(self):
        playable_cards = [
            card
            for card in self.computer_hand
            if card[0] == self.tablecard[-1][0]
            or card[1] == self.tablecard[-1][1]
            or card[0] == "joker"
            or card[1] == "joker"
        ]
        if not self.deck:
            return {"message":"deck is empty"}

        if playable_cards:
            play = random.choice(playable_cards)
            self.tablecard.append(play)
            self.computer_hand.remove(play)

            if play[0] in ["2", "3"]:
                penalty_cards = 2 if play[0] == "2" else 3
                for _ in range(penalty_cards):
                    if self.deck:
                        self.player_hand.append(self.deck.pop())

            if play[0] in ["K", "Q", "J", "8"]:
               pass

            if play[0] == "joker" or play[1] == "joker":
                for _ in range(5):
                    if self.deck:
                        self.player_hand.append(self.deck.pop())
        
    
        else :
            self.computer_hand.append(self.deck.pop())
            return {"message": "Computer picked a move"}
        return {
            "computer_hand": self.computer_hand,
            "player_hand": self.player_hand,
            "table_card": self.tablecard,
        }

    def new_game(self, player_id, computer_id):
    
        self.create_deck()
        self.deal_cards()
        new_game = Game(
            deck=self.deck,
            computer_id=player_id,
            player_id=computer_id,
            table_card=self.tablecard,
        )

        db.session.add(new_game)
        db.session.commit()

        related_player = Player.query.get(player_id)

        return {
            "game": {
                # "deck": new_game.deck,
                "table_card": new_game.table_card,
                "player": new_game.player_id,
                "related_player": {
                    "id": related_player.id,
                    "name": related_player.name,
                    "cards": self.player_hand,
                },
                "computer": {"cards": self.computer_hand},
            }
        }
    
    def reset_cards(self):
        self.player_hand=[]
        self.computer_hand = []
        self.tablecard = []
        return {
            "player":self.player_hand,
            "computer":self.computer_hand,
            "deck": self.tablecard
        }
    def reset_deck(self):
        self.deck = []
     