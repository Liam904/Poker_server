from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from .models import db
from flask_cors import CORS

bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = "secret_key"

    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    from app.auth_routes import auth
    from app.game_routes import game
    app.register_blueprint(auth)
    app.register_blueprint(game)

    return app
