from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse

from ..utils.validators import AuthValidators, GeneralValidators
from ..auth.models import AuthModel


class Signup(Resource):
    """signup endpoint resource"""
    parser = reqparse.RequestParser()
    parser.add_argument("firstname",
                        type=str,
                        required=True,
                        nullable=False,)
    parser.add_argument("lastname",
                        type=str,
                        required=True,
                        nullable=False,)
    parser.add_argument("email",
                        type=str,
                        required=True,
                        nullable=False,)
    parser.add_argument("password",
                        type=str,
                        required=True,
                        nullable=False,)
    parser.add_argument("phonenumber",
                        type=str)

    @staticmethod
    def post():
        """
        Register User
        ---
            tags:
            - auth
            consumes:
            - application/json
            parameters:
            - in: body
              name: Register a new user
              description: Signup new user with their email and password
              schema:
                id: Register User
                type: object
                required:
                - email
                - password
                - firstname
                - lastname
                - phonenumber
                properties:
                  firstname:
                    type: string
                  lastname:
                    type: string
                  email:
                    type: string
                  password:
                    type: string
                  phonenumber:
                    type: string
            responses:
              201:
                description: User registered successfully
              400:
                description: Invalid data format
              409:
                description: A user with that email already exists
        """
        data = Signup.parser.parse_args()

        GeneralValidators.non_empty_string(**data)

        AuthValidators.check_email_format(data["email"])

        AuthValidators.check_email_exists(data["email"])

        AuthValidators.check_password_length(data["password"])

        user = AuthModel(**data)
        user.save_to_db()

        response = {
            "status": 201,
            "message": "user registered successfully",
            "data": [{
                "access_token": create_access_token(data["email"])
                }]}

        return response, 201
