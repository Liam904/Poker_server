from .game_logic import ranks, suits
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.String(10), nullable=False)
    suit = db.Column(db.String(10), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=True)

        

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100),  nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cards = db.relationship('Card', backref='player', lazy=True)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deck = db.Column(db.PickleType, nullable=False)
    table_card = db.Column(db.PickleType, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    computer_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)