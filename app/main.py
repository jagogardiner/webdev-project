from flask import Blueprint
from . import db

app = Blueprint('app', __name__)

from app import routes
