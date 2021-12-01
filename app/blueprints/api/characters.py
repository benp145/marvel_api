from app.blueprints.characters.models import Character
from .import bp as characters
from flask import jsonify
from .auth import token_auth

@characters.route('/characters/<int:id>', methods=['GET'])
@token_auth.login_required
def get_character(id):
    return jsonify(Character.query.get(id).to_dict())