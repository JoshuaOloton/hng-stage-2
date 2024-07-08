from . import auth
from flask import jsonify, request
from api.models import User, Organisation
from api import bcrypt, db
from api.utils import validate_register_fields, validate_login_fields
from flask_jwt_extended import create_access_token
from datetime import timedelta
import uuid


expiration_delta = timedelta(minutes=15)

@auth.route('/login', methods=['POST'])
def login():
    try:
        if not request.data:
            return jsonify({"error": "Request must be non-empty JSON"}), 400
        
        json_body = request.json

        email = json_body.get('email')
        password = json_body.get('password')

        errors = validate_login_fields(json_body)
        if len(errors) > 0:
            return jsonify({"errors": errors}), 422

        # if not email or not password:
        #     return jsonify({'error': 'Missing field'})

        existing_user = User.query.filter_by(email=email).first()

        if existing_user and existing_user.verify_password(password):
            access_token = create_access_token(identity=email, expires_delta=expiration_delta)
            return jsonify({
                "status": "success",
                "message": "Login successful",
                "data": {
                    "accessToken": access_token,
                    "user": existing_user.to_json()
                }
            }), 200
        
        raise Exception

    except Exception as e:
        return jsonify({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": "401"
        }), 401
    

@auth.route('/register',  methods=['POST'])
def register():
    try:
        if not request.data:
            return jsonify({"error": "Request must be non-empty JSON"}), 400
        
        json_body = request.json
        
        firstName = json_body.get('firstName')
        lastName = json_body.get('lastName')
        email = json_body.get('email')
        password = json_body.get('password')
        phone = json_body.get('phone')

        errors = validate_register_fields(json_body)
        if len(errors) > 0:
            return jsonify({"errors": errors}), 422

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8') # hash password before storing in db

        userid = str(uuid.uuid4())
        while User.query.get(userid):
            userid = str(uuid.uuid4())  # ensure userId is unique

        user = User(
            userId=userid,
            firstName=firstName.capitalize(), 
            lastName=lastName,
            email=email,
            password_hash=password_hash,
            phone=phone
        )

        # once user is registered, create an access token for immediate login
        access_token = create_access_token(identity=email, expires_delta=expiration_delta)

        # create an organisation for the user
        orgid = str(uuid.uuid4())
        while Organisation.query.get(orgid):
            orgid = str(uuid.uuid4())  # ensure orgid is unique

        organisation = Organisation(
            orgId = orgid,
            name= f'{firstName.capitalize()}\'s Organisation',
        )
        user.organisations.append(organisation)

        db.session.add(user)
        db.session.add(organisation)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Registration successful",
            "data": {
                "accessToken": access_token,
                "user": user.to_json()
            }
            }), 201

        # return jsonify(user.to_json()), 201

    except Exception:
        return jsonify({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": "400"
        }), 400
