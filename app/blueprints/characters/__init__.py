from flask import Blueprint

bp = Blueprint('characters', __name__, url_prefix="/characters")

from . import routes, models