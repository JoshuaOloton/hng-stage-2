from . import main
from flask import jsonify
from flask_jwt_extended import jwt_required


@main.route('/')
def index():
    return 'Hello World! This is the HNG11 Backend Track Stage 2 Task.'

@main.route('/protected')
@jwt_required()
def protected():
    return jsonify({'message': 'This is a protected route!'})
