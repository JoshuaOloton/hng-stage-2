from . import organisations
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.models import Organisation, User
from api import db
import uuid


@organisations.route('/organisations', methods=['GET'])
@jwt_required()
def get_orgs():
    try:
        # get current logged in user
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        user_orgs = current_user.organisations

        return jsonify({
            "status": "success",
            "message": "Request successful",
            "data": {
                "organisations": [org.to_json() for org in user_orgs]
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "Bad request",
            "message": f"{e}",
            "statusCode": "500"
        }), 400
    

# get a single organisation record for a logged in user
@organisations.route('/organisations/<orgId>', methods=['GET'])
@jwt_required()
def get_org(orgId):
    try:
        # get current logged in user
        current_user = User.query.filter_by(email=get_jwt_identity()).first()
        org = Organisation.query.get(orgId)

        # Check if current user is authorized to access the organization
        if org not in current_user.organisations:
            return jsonify({
                "status": "Unauthorized",
                "message": "Unauthorized to access organisation",
                "statusCode": "401"
            }), 401
    
        return jsonify({
            "status": "success",
            "message": "Request successful",
            "data": {
                "organisation": org.to_json()
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "Bad request",
            "message": f"{e}",
            "statusCode": "500"
        }), 400
    

# create a new organisation
@organisations.route('/organisations', methods=['POST'])
@jwt_required()
def post_org():
    try:
        if not request.data:
            return jsonify({"error": "Request must be non-empty JSON"}), 400

        name = request.json.get('name')
        description = request.json.get('description')

        # validate json body
        if name is None or name == '':
           return jsonify({
               "errors": {
                   "field": "name",
                    "message": "name cannot be null"
               }
               }), 422

        # get current logged in user
        current_user = User.query.filter_by(email=get_jwt_identity()).first()

        orgid = str(uuid.uuid4())
        while Organisation.query.get(orgid):
            orgid = str(uuid.uuid4())  # ensure orgid is unique

        organisation = Organisation(
            orgId = orgid,
            name=name, 
            description=description
        )

        current_user.organisations.append(organisation)

        db.session.add(organisation)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Organisation created successfully",
            "data": {
                "organisation": organisation.to_json()
            }
        }), 201
    
    except Exception:
        return jsonify({
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }), 400

# add user to a particular organisation
@organisations.route('/organisations/<orgId>/users', methods=['POST'])
@jwt_required()
def add_user_to_org(orgId):
    try:
        if not request.data:
            return jsonify({"error": "Request must be non-empty JSON"}), 400
        
        organisation = Organisation.query.get(orgId)
        userId = request.json.get("userId")

        # Validate json body
        if userId is None or userId == '':
           return jsonify({
               "errors": {
                   "field": "userId",
                    "message": "userId cannot be null"
               }
               }), 422

        user = User.query.get(userId)
        if user is None:
            return jsonify({
                "message": "User not found"
            }), 404
        
        user.organisations.append(organisation)

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "User added to organisation successfully",
        }), 200
    
    except Exception:
        return jsonify({
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400
        }), 400