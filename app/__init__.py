from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

# Create extensions
db = SQLAlchemy()
mail = Mail()
moment = Moment()


def create_app(config_name):
    # Create & configure app
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Init extensions
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    # Import & register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
