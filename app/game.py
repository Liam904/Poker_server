import random
from app.models import Card, Game, db, Player
from flask import jsonify

class GameEngine:
    def __init__(self):
        self.deck = []
        self.player_hand = []
        self.computer_hand = []
        self.table_card = []

    def create_deck(self):
        cards = Card.query.all()
        self.reset_deck()
        self.deck = [(card.rank, card.suit) for card in cards]
        random.shuffle(self.deck)
        return self.deck

    def deal_cards(self):
        self.create_deck()
        self.reset_cards()
        
        for _ in range(4):
            self.player_hand.append(self.deck.pop())
            self.computer_hand.append(self.deck.pop())
        
        self.table_card.append(self.deck.pop())
        return {
            "player_hand": self.player_hand,
            "computer_hand": self.computer_hand,
            "table_card": self.table_card,
        }

    def player_moves(self, rank, suit):
        play = (rank, suit)
        if play in self.player_hand and (
            play[0] == self.table_card[-1][0] or play[1] == self.table_card[-1][1]
        ):
            self.table_card.append(play)
            self.player_hand.remove(play)
            penalty = []
            if play[0] in ["2", "3"]:
                for _ in range(2):
                    card = self.deck.pop()
                    self.computer_hand.append(card)
                    penalty.append(card)

            
            return {
                "computer_hand":self.computer_hand,
                "valid":True,
                "penalty":penalty
            }
        else:
            return {
                "valid":False
            }


    def new_game(self, player_id, computer_id):
        new_game = Game(
            deck=self.deck,
            computer_id=computer_id,
            player_id=player_id,
            table_card=self.table_card,
        )
        db.session.add(new_game)
        db.session.commit()
        related_player = Player.query.get(player_id)
        return {
            "table_card": new_game.table_card,
            "player": {
                "id": related_player.id,
                "name": related_player.name,
                "cards": self.player_hand,
            },
            "computer": self.computer_hand,
        }

    def reset_cards(self):
        self.player_hand = []
        self.computer_hand = []
        self.table_card = []
        return {
            "player": self.player_hand,
            "computer": self.computer_hand,
            "table_card": self.table_card,
        }

    def reset_deck(self):
        self.deck = []