# HNG STAGE 2 TASK

This project provides authentication endpoints for user registration and login. The API is built using Flask and includes user validation, password hashing, and JWT token generation.

## Endpoints

### `/login`

**Method:** `POST`

This endpoint allows users to log in to the application.

#### Request

- **URL:** `/login`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
- **Body:**
  ```json
  {
      "email": "user@example.com",
      "password": "userpassword"
  }
  ```

### Responses
- **Success (200)**

  ```
  {
    "status": "success",
    "message": "Login successful",
    "data": {
        "accessToken": "JWT_TOKEN_HERE",
        "user": {
            "userId": "USER_ID",
            "firstName": "UserFirstName",
            "lastName": "UserLastName",
            "email": "user@example.com",
            "phone": "1234567890"
        }
    }
  }
  ```
- **Error (400)**

  ```
  {
    "error": "Request must be non-empty JSON"
  }
  ```

- **Error (401)**

  ```
  {
    "status": "Bad request",
    "message": "Authentication failed: ERROR_MESSAGE",
    "statusCode": "401"
  }
  ```

### `/register`
This endpoint allows users to register a new account in the application.

#### Request

- **URL:** `/register`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
- **Body:**

  ```json
  {
    "firstName": "FirstName",
    "lastName": "LastName",
    "email": "user@example.com",
    "password": "userpassword",
    "phone": "1234567890"
  }
  ```

### Responses
- **Success (201)**

  ```
  {
    "status": "success",
    "message": "Registration successful",
    "data": {
        "accessToken": "JWT_TOKEN_HERE",
        "user": {
            "userId": "USER_ID",
            "firstName": "FirstName",
            "lastName": "LastName",
            "email": "user@example.com",
            "phone": "1234567890"
        }
    }
  }
  ```

- **Error (400)**

  ```
  {
      "status": "Bad request",
      "message": "Registration unsuccessful",
      "statusCode": "400"
  }
  ```

- **Error (422)**

  ```
  {
    "errors": [
        "Field validation errors"
    ]
  }
  ```

### `/organisations`
This endpoint retrieves all organisations associated with the logged-in user.

#### Request

- **URL:** `/organisations`
- **Method:** `GET`
- **Headers:**
  - `Authorization: Bearer JWT_TOKEN_HERE`


### Responses
- **Success (200)**

  ```
  {
    "status": "success",
    "message": "Request successful",
    "data": {
        "organisations": [
            {
                "orgId": "ORG_ID",
                "name": "OrganisationName",
                "description": "OrganisationDescription"
            },
            {
                "orgId": "ORG_ID",
                "name": "OrganisationName",
                "description": "OrganisationDescription"
            }
        ]
    }
  }
  ```

- **Error (400)**

  ```
  {
    "status": "Bad request",
    "message": "ERROR_MESSAGE",
    "statusCode": "400"
  }
  ```

### `/organisations/<orgId>`
This endpoint retrieves a specific organisation's details for the logged-in user.

#### Request

- **URL:** `/organisations/<orgId>`
- **Method:** `GET`
- **Headers:**
  - `Authorization: Bearer JWT_TOKEN_HERE`


### Responses
- **Success (200)**

  ```
  {
    "status": "success",
    "message": "Request successful",
    "data": {
        "organisation": {
            "orgId": "ORG_ID",
            "name": "OrganisationName",
            "description": "OrganisationDescription"
        }
    }
  }
  ```

- **Error (400)**

  ```
   {
    "status": "Bad request",
    "message": "ERROR_MESSAGE",
    "statusCode": 400"
  }
  ```

- **Error (401)**

  ```
  {
    "status": "Unauthorized",
    "message": "Unauthorized to access organisation",
    "statusCode": "401"
  }
  ```

### `/organisations`
This endpoint allows the logged-in user to create a new organisation.

#### Request

- **URL:** `/organisations`
- **Method:** `POST`
- **Headers:**
  - `Content-Type: application/json`
  - `Authorization: Bearer JWT_TOKEN_HERE`
- **Body:**

  ```json
  {
    "name": "OrganisationName",
    "description": "OrganisationDescription"
  }
  ```

### Responses
- **Success (201)**

  ```
  {
    "status": "success",
    "message": "Organisation created successfully",
    "data": {
        "organisation": {
            "orgId": "ORG_ID",
            "name": "OrganisationName",
            "description": "OrganisationDescription"
        }
    }
  }
  ```

- **Error (422)**

  ```
  {
    "errors": {
        "field": "name",
        "message": "name cannot be null"
    }
  }
  ```

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. Create a virtual environment and activate it:
    ```python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```


3. Install dependencies

    ```
    pip install -r requirements.txt
    ```



## Running the Application
### Start the Flask development server:

```
flask run
```

### Dependencies

- Python 3.x
- Flask
- Flask SQLAlchemy
- Flask JWT Extended
- Flask BCrypt

### Live URL: https://hng-stage-1-weld.vercel.app/api/


