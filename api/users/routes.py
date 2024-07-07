from . import users
from flask_jwt_extended import jwt_required

@users.route('/users', methods=['GET'])
def get_users():
    return 'Users route'


@users.route('/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user(id):
    return 'User route'