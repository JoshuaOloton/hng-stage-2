from . import users
from api.models import User
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


@users.route('/users/<userId>', methods=['GET'])
@jwt_required()
def get_user(userId):
    # get current logged in user
    current_user = User.query.filter_by(email=get_jwt_identity()).first()
    if userId == current_user.userId:
        return jsonify({
            "status": "success",
            "message": "Request successful",
            "data": {
                "user": current_user.to_json()
            }
        }), 200
    
    user = User.query.get(userId)
    if current_user.has_common_organisation(user):
        return jsonify({
            "status": "success",
            "message": "Request successful",
            "data": {
                "user": user.to_json()
            }
        }), 200

    return jsonify({
        "status": "Unauthorized",
        "message": "Unauthorized to access user",
        "statusCode": "401"
    }), 401