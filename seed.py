from app.models import Card, db, Game, Player
from app import create_app

app = create_app()


with app.app_context():
    Card.query.delete()
    Game.query.delete()
    Player.query.delete()

    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]


    for rank in ranks:
        for suit in suits:
            card = Card(rank=rank, suit=suit)
            db.session.add(card)
    
    db.session.commit()
