from datetime import datetime, timedelta
from flask_jwt_extended import decode_token
from api.models import User, Organisation

def test_token_generation(client, app):
    client.post('/api/register', json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password",
        "phone": "123-456-6890"
    })

    response = client.post('/api/login', json={
        "email": "john.doe@example.com",
        "password": "password"
    })

    expiration_delta = timedelta(minutes=15)
    now = datetime.now().replace(microsecond=0)

    data = response.get_json()
    assert response.status_code == 200

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = expiration_delta
    access_token = data['data']['accessToken']
    decoded_token = decode_token(access_token)

    expiration = decoded_token['exp']
    expiration_datetime = datetime.fromtimestamp(expiration)

    # Ensure token expires at the correct time and correct user details is found in token.
    assert (now + expiration_delta) <= expiration_datetime

    assert decoded_token['sub'] == 'john.doe@example.com'


def test_organisations(client, app):
    # register two new users i.e John and Jake
    client.post('/api/register', json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password",
        "phone": "123-456-6890"
    })

    client.post('/api/register', json={
        "firstName": "Jake",
        "lastName": "Paul",
        "email": "jake.paul@example.com",
        "password": "password",
        "phone": "123-456-6890"
    })

    # login the first user
    client.post('/api/login', json={
        "email": "john.doe@example.com",
        "password": "password"
    })

    # try and access second user's organisation i.e. Jake's organisation
    with app.app_context():
        org = Organisation.query.filter_by(name="Jake's Organisation").first()
        orgId = org.orgId

    response = client.get(f'/api/organisations/{orgId}')

    # assert 401 unauthorised error
    assert response.status_code == 401


def test_full_registration(client, app):
    response = client.post('/api/register', json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password",
        "phone": "123-456-6890"
    })

    # ensure user is registered successfully
    assert response.status_code == 201

    # ensure defailt organisation is correctly generated
    with app.app_context():
        user_org = Organisation.query.filter_by(name="John's Organisation").first()
        assert user_org is not None

    # check that response contains expect user details and access token
    data = response.get_json()
    assert data['data']['user']['firstName'] == 'John'
    assert data['data']['user']['lastName'] == 'Doe'
    assert data['data']['user']['email'] == 'john.doe@example.com'
    assert 'accessToken' in data['data']

    # ensure user logs in sucessfully using correct cresentials and fails otherwise
    response = client.post('/api/login', json={
        "email": "john.doe@example.com",
        "password": "password"
    })
    assert response.status_code == 200

    # check that response contains expect user details and access token
    data = response.get_json()
    assert data['data']['user']['firstName'] == 'John'
    assert data['data']['user']['lastName'] == 'Doe'
    assert data['data']['user']['email'] == 'john.doe@example.com'
    assert 'accessToken' in data['data']

    # provide false email
    response = client.post('/api/login', json={
        "email": "john.doe@example.com",
        "password": "falsepassword"
    })
    assert response.status_code == 401

    # provide false password
    response = client.post('/api/login', json={
        "email": "wrongemail@example.com",
        "password": "password"
    })
    assert response.status_code == 401

    # ensure registration fails when required fields are not provided

    # missing firstName
    response = client.post('/api/register', json={
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password",
        "phone": "123-456-6890"
    })
    data = response.get_json()
    assert response.status_code == 422 and data['errors'][0]['message'] == 'firstName must not be null or empty'

    # missing lastName
    response = client.post('/api/register', json={
        "firstName": "John",
        "email": "john.doe@example.com",
        "password": "password",
        "phone": "123-456-6890"
    })
    data = response.get_json()
    assert response.status_code == 422 and data['errors'][0]['message'] == 'lastName must not be null or empty'

    # missing email
    response = client.post('/api/register', json={
        "firstName": "John",
        "lastName": "Doe",
        "password": "password",
        "phone": "123-456-6890"
    })
    data = response.get_json()
    assert response.status_code == 422 and data['errors'][0]['message'] == 'email must not be null or empty'

    # missing password
    response = client.post('/api/register', json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "phone": "123-456-6890"
    })
    data = response.get_json()
    assert response.status_code == 422 and data['errors'][0]['message'] == 'password must not be null or empty'


    # ensure registration fails when there's duplicate email or userID
    response = client.post('/api/register', json={
        "firstName": "John",
        "lastName": "Doe",
        "email": "john.doe@example.com",
        "password": "password",
        "phone": "123-456-6890"
    })
    data = response.get_json()
    assert response.status_code == 422 and data['errors'][0]['message'] == 'email must be unique'

