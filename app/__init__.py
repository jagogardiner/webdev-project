import os
from flask import Flask, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# Class-based application configuration
db = SQLAlchemy()


class ConfigClass(object):
    """Flask application config"""

    TEMPLATES_AUTO_RELOAD = True

    # Flask settings
    load_dotenv()
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    # Flask-SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning

    # Flask-User settings
    USER_ENABLE_EMAIL = False  # Disable email authentication
    USER_ENABLE_USERNAME = True  # Enable username authentication
    USER_REQUIRE_RETYPE_PASSWORD = False  # Simplify register form

    # Client directories
    CLIENT_PDF = "app/static/client/pdf/"


# Error handler for 404


def page_not_found(e):
    return render_template("error.html"), 404


def internal_server_error(e):
    flash(
        "There was an internal error - please contact an administrator if this problem"
        " persists."
    )
    return render_template("error.html"), 500


def not_authorized(e):
    flash("You are not authorized to view this page.")
    return render_template("home.html"), 403


def create_app():
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, not_authorized)
    app.register_error_handler(500, internal_server_error)

    app.config.from_object(__name__ + ".ConfigClass")
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    # blueprint for auth routes in our app
    from .auth_routes import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import app as app_blueprint

    app.register_blueprint(app_blueprint)

    # blueprint for api routes
    from .api_routes import api as api_blueprint

    app.register_blueprint(api_blueprint)

    from .model import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
