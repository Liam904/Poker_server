from flask import jsonify, Blueprint, request
import random
from .models import Card, Game, db, Player

game = Blueprint("game", __name__)

deck = []
player_hand = []
computer_hand = []
tablecard = []


@game.route("/game/deck", methods=["GET"])
def create_deck():
    global deck
    card = Card.query.all()

    card_list = []
    for cards in card:
        deck = (cards.rank, cards.suit)
        card_list.append(deck)

    random.shuffle(card_list)

    deck = card_list
    # print(deck)
    return jsonify(card_list)


@game.route("/game/deal_cards", methods=["GET"])
def deal_cards():
    global deck
    if not deck:
        return jsonify({"Message": "No deck found"})

    for _ in range(4):
        player_hand.append(deck.pop())
        computer_hand.append(deck.pop())

    tablecard.append(deck.pop())

    return jsonify(
        {"player": player_hand, "computer_hand": computer_hand, "table_card": tablecard}
    )


@game.route("/game/playermoves", methods=["POST"])
def playerMoves():
    body = request.get_json()
    rank = body.get("rank")
    suit = body.get("suit")
    global player_hand, tablecard
    play = (rank, suit)
    if play in player_hand and (
        play[0] == tablecard[-1][0] or play[1] == tablecard[-1][1]
    ):
        tablecard.append(play)
        player_hand.remove(play)
        print(player_hand)
        print(tablecard)
        if play[0] in ["2", "3", "Q", "J", "K", "8", "9"]:
            print("Working fine")

    return jsonify({"player_hand": player_hand, "table_card": tablecard})

@game.route("/game/computerMoves", methods=['GET'])
def computer_moves():
    global computer_hand, tablecard, deck, player_hand

    playable_cards = [card for card in computer_hand 
                      if card[0] == tablecard[-1][0] or card[1] == tablecard[-1][1]]

    if playable_cards:
        play = random.choice(playable_cards)
        print(f"Computer played: {play}")

        tablecard.append(play)
        computer_hand.remove(play)

        if play[0] in ["2", "3"]:
            penalty_cards = 2 if play[0] == "2" else 3
            for _ in range(penalty_cards):
                if deck:
                    player_hand.append(deck.pop())
            print("Penalty! Cards added")

        elif play[0] in ["K", "Q", "J", "8"]:
            computer_moves()
            playerMoves()

        elif play[0] == "joker" or play[1] == "joker":
            for _ in range(5):
                if deck:
                    player_hand.append(deck.pop())



    return jsonify({"computer_hand": computer_hand, "table_card": tablecard})



@game.route("/game/new_game", methods=["POST"])
def new_game():
    create_deck()
    deal_cards()
    print(player_hand)
    print(computer_hand)
    
    body = request.get_json()
    player_id = body.get("player_id")
    computer_id = body.get("computer_id")
    global deck, tablecard
    new_game = Game(
        deck=deck, computer_id=computer_id, player_id=player_id, table_card=tablecard
    )

    db.session.add(new_game)
    db.session.commit()

    related_player = Player.query.get(player_id)
    
    return jsonify(
        {
            "game": {
                "deck": new_game.deck,
                "table_card": new_game.table_card,
                "rel_player": new_game.player_id,
                "related_player": {"name": related_player.name, "cards": player_hand},
                "computer":{
                    "cards":computer_hand
                }
            }
        }
    )

        


