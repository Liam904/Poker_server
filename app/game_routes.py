from flask import jsonify, Blueprint, request
from .game import GameEngine
from flask_jwt_extended import jwt_required, get_jwt_identity

game = Blueprint("game", __name__)


game_engine = GameEngine()


@game.route("/game/deck", methods=["GET"])
@jwt_required()
def create_deck():
    return jsonify(game_engine.create_deck())


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
    return jsonify(game_engine.player_moves(rank, suit))


@game.route("/game/computer_moves", methods=["GET"])
@jwt_required()
def computer_moves():
    return jsonify(game_engine.computer_moves())


@game.route("/game/new_game", methods=["POST"])
@jwt_required()
def new_game():
    player = get_jwt_identity()
    computer_id = 1
    print(player)
    return jsonify(game_engine.new_game(player, computer_id))
