from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

from ..utils.validators import AuthValidators
from ..utils.error_handlers import UserLoginError
from ..auth.models import AuthModel


class Login(Resource):
    """login endpoint resource"""
    parser = reqparse.RequestParser()
    parser.add_argument("email",
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    @staticmethod
    def post():
        """do a POST to login endpoint"""
        data = Login.parser.parse_args()

        AuthValidators.check_email_format(data["email"])

        AuthValidators.confirm_login_email(data["email"])

        AuthModel.verify_hash(data["email"], data["password"])

        response = {
            "status": 200,
            "message": "user logged in successfully",
            "data": [{
                "access_token": create_access_token(data["email"])
            }]}

        return response, 200
        # else:
        #     raise UserLoginError
