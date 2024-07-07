from . import auth
from flask import jsonify, request
from api.models import User, Organisation
from api import bcrypt, db
from api.utils import validate_auth_fields
from flask_jwt_extended import create_access_token
import sqlalchemy

@auth.route('/login', methods=['POST'])
def login():
    try:
        if not request.data:
            return jsonify({"error": "Request must be non-empty JSON"}), 400

        email = request.json['email']
        password = request.json['password']
        print('Email: ', email)
        print('Password: ', password)

        if not email or not password:
            return jsonify({'error': 'Missing field'})

        existing_user = User.query.filter_by(email=email).first()

        if existing_user and existing_user.verify_password(password):
            access_token = create_access_token(identity=email,)
            return jsonify({
                "status": "success",
                "message": "Login successful",
                "data": {
                    "access_token": access_token,
                    "user": existing_user.to_json()
                }
            }), 200
        
        raise Exception

    except Exception as e:
        return jsonify({
            "status": "Bad request",
            "message": f"Authentication failed: {e}",
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

        errors = validate_auth_fields(json_body)
        if len(errors) > 0:
            return jsonify({"errors": errors}), 422

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8') # hash password before storing in db

        user = User(
            firstName=firstName.capitalize(), 
            lastName=lastName,
            email=email,
            password_hash=password_hash,
            phone=phone
        )

        # once user is registered, create an access token for immediate login
        access_token = create_access_token(identity=email)

        # create an organisation for the user
        organisation = Organisation(
            name= f'{firstName.capitalize()}\'s Organisation',
        )
        user.organisations.append(organisation)

        db.session.add(user)
        db.session.add(organisation)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Login successful",
            "data": {
                "access_token": access_token,
                "user": user.to_json()
            }
            }), 201

        # return jsonify(user.to_json()), 201

    except sqlalchemy.exc.IntegrityError as e:
        errorInfo = e.orig.args
        print('ErrorInfo')  #This will give you error code
        print(errorInfo)  #This will give you error code
        print(e)
        # print(errorInfo[1])
        # print(e.orig.diag.message_detail) 
        return jsonify({
            "status": "Bad request",
            "message": f"{e}",
            "statusCode": "400"
        }), 400

    except Exception:
        return jsonify({
            "status": "Bad request",
            "message": "Registration unsuccessful",
            "statusCode": "400"
        }), 400

@auth.route('/logout')
def logout():
    return jsonify({'message': 'Logout route works!'})