from api.models import User
import re


def is_empty(data):
    return data == '' or data is None

def validate_login_fields(json_body):
    email_regex =  r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    errors = []

    required_fields = ["email", "password"]

    for field in required_fields:
        if field not in json_body or is_empty(json_body.get(field)):
            errors.append({
                "field": field,
                "message": f"{field} must not be null or empty"
            })

        if json_body.get(field) and not isinstance(json_body.get(field), str):
            errors.append({
                "field": field,
                "message": f"{field} must be a string"
            })

    if json_body.get('email') and re.match(email_regex, json_body.get('email')) is None:
        errors.append({
            "field": "email",
            "message": "invalid email address"
        })
    
    return errors


def validate_register_fields(json_body):
    email_regex =  r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    errors = []

    required_fields = ["firstName", "lastName", "email", "password"]

    for field in required_fields:
        if field not in json_body or is_empty(json_body.get(field)):
            errors.append({
                "field": field,
                "message": f"{field} must not be null or empty"
            })

        if json_body.get(field) and not isinstance(json_body.get(field), str):
            errors.append({
                "field": field,
                "message": f"{field} must be a string"
            })

    if json_body.get('phone') and not isinstance(json_body.get('phone'), str):
        errors.append({
            "field": "phone",
            "message": "phone must be a string"
        })

    if json_body.get('email') and re.match(email_regex, json_body.get('email')) is None:
        errors.append({
            "field": "email",
            "message": "invalid email address"
        })

    if  json_body.get('email') and User.query.filter_by(email=json_body.get('email')).first():
        errors.append({
            "field": "email",
            "message": "email must be unique"
        })

    return errors


def validate_organisation_fields(json_body):
    errors = []

    if "name" not in json_body or is_empty(json_body.get("name")):
        errors.append({
            "field": "name",
            "message": "name must not be null or empty"
        })

    if json_body.get("name") and not isinstance(json_body.get("name"), str):
        errors.append({
            "field": "name",
            "message": "name must be a string"
        })
    if json_body.get("description") and not isinstance(json_body.get("description"), str):
        errors.append({
            "field": "description",
            "message": "description must be a string"
        })

    return errors