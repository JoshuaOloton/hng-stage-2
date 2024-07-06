from . import auth
from flask import jsonify, request
from api.models import User, Organization
from api import bcrypt, db
from flask_jwt_extended import create_access_token

@auth.route('/login', methods=['POST'])
def login():
    try:
        email = request.json['email']
        password = request.json['password']

        if not email or not password:
            return jsonify({'error': 'Missing field'})

        existing_user = User.query.filter_by(email=email).first()

        if existing_user and User.verify_password(password):
            access_token = create_access_token(identity=email)
            return jsonify({
                'message': 'Login successful!',
                'access_token': access_token
            }), 200
        
        return jsonify({'message': 'Invalid email or password!'}), 401

    except Exception as e:
        pass

@auth.route('/register',  methods=['POST'])
def register():
    try:
        firstName = request.json['firstName']
        lastName = request.json['lastName']
        email = request.json['email']
        password = request.json['password']
        phone = request.json['phone']

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(
            firstName=firstName, 
            lastName=lastName,
            email=email,
            password_hash=password_hash,
            phone=phone
        )

        organization = Organization(
            name= f'{firstName}\'s Organization',
            description='A tech company that provides opportunities for young developers to grow.'
        )

        db.session.add(user)
        db.session.commit()

        return jsonify(user.to_dict()), 201

    except Exception as e:
        return jsonify({'message': f'Invalid request: {e}'})

@auth.route('/logout')
def logout():
    return jsonify({'message': 'Logout route works!'})