from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app) 
    moment.init_app(app)

    from app.blueprints.main import bp as main
    app.register_blueprint(main)

    from app.blueprints.auth import bp as auth
    app.register_blueprint(auth)

    from app.blueprints.characters import bp as characters
    app.register_blueprint(characters)

    from app.blueprints.users import bp as users
    app.register_blueprint(users)

    from app.blueprints.api import bp as api
    app.register_blueprint(api)



    return app