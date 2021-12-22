from flask import Blueprint

app = Blueprint("app", __name__)

# flake8: noqa
from app import routes
