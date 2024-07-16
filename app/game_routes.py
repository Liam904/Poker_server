from flask import jsonify, Blueprint, request
from .game import GameEngine
import random 
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Game
game = Blueprint("game", __name__)


game_engine = GameEngine()


## code renders in the dashboard to display the players' cards
@game.route("/game/deal_cards", methods=["GET"])
@jwt_required()
def deal_cards():
   return jsonify(game_engine.deal_cards())



@game.route("/game/playermoves", methods=["POST"])
@jwt_required()
def player_moves():
    body = request.get_json()
    rank = body.get("rank")
    suit = body.get("suit")
    return game_engine.player_moves(rank, suit)
    



@game.route("/game/new_game", methods=["POST"])
@jwt_required()
def new_game():
    current_user = get_jwt_identity()
    computer_id = random.randint(1, 10)
    return jsonify(game_engine.new_game(player_id=current_user, computer_id=computer_id))
