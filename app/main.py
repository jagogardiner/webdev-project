from flask import Blueprint

app = Blueprint('app', __name__)

from app import routes