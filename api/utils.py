from api.models import User


def is_empty(data):
    return data == '' or data is None

def validate_auth_fields(json_body):
    errors = []

    required_fields = ["firstName", "lastName", "email", "password"]

    for field in required_fields:
        if field not in json_body or is_empty(json_body[field]):
            errors.append({
                "field": field,
                "message": f"{field} must not be null or empty"
            })

    if  User.query.filter_by(email=json_body.get('email')).first():
        errors.append({
            "field": "email",
            "message": "Email must be unique"
        })

    return errors


def validate_organisation_fields(json_body):
    errors = []

    required_fields = ["name", "description"]

    for field in required_fields:
        if field not in json_body or is_empty(json_body[field]):
            errors.append({
                "field": field,
                "message": f"{field} must not be null or empty"
            })

    return errors