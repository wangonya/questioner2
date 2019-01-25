from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse

from ..utils.validators import AuthValidators, GeneralValidators
from ..auth.models import AuthModel


class Signup(Resource):
    """signup endpoint resource"""
    parser = reqparse.RequestParser()
    parser.add_argument("firstname",
                        type=GeneralValidators.non_empty_string,
                        required=True,
                        nullable=False,)
    parser.add_argument("lastname",
                        type=GeneralValidators.non_empty_string,
                        required=True,
                        nullable=False,)
    parser.add_argument("email",
                        type=str,
                        required=True,
                        nullable=False,)
    parser.add_argument("password",
                        type=GeneralValidators.non_empty_string,
                        required=True,
                        nullable=False,)
    parser.add_argument("phonenumber",
                        type=str)

    @staticmethod
    def post():
        """do a POST to signup endpoint"""
        data = Signup.parser.parse_args()

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
