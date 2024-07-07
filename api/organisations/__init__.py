from flask import Blueprint

organisations = Blueprint('organisations', __name__)

from . import routes