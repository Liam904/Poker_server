from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token
from app import bcrypt
from .models import Player, db

auth = Blueprint('auth', __name__)


@auth.route("/signup", methods=['POST'])
def signup():
    body = request.get_json()
    email = body.get('email')
    name = body.get("name")
    password = body.get("password")
    password = str(password)
    if not email or not name or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    if Player.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_player = Player(name=name, email=email, password=hashed_password)

    db.session.add(new_player)
    db.session.commit()

    return jsonify({
        "name": new_player.name,
        "email": new_player.email
    }), 201

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    password = str(password)

    if not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    player = Player.query.filter_by(email=email).first()

    if player and bcrypt.check_password_hash(player.password, password):
        access_token = create_access_token(identity=player.id)
        refresh_token = create_refresh_token(identity=player.id)
        return jsonify({
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200

    return jsonify({"msg": "Invalid email or password"}), 401
