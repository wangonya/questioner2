from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

from ..utils.validators import AuthValidators
from ..auth.models import AuthModel
from ..db.select import SelectDataFromDb


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

        is_admin = SelectDataFromDb.conditional_where_and_select("users", "email", data["email"], "is_admin", True)

        try:
            response = {
                "status": 200,
                "message": "user logged in successfully",
                "data": [{
                    "access_token": create_access_token(data["email"]),
                    "is_admin": is_admin["is_admin"]
                }]}
        except TypeError:
            response = {
                "status": 200,
                "message": "user logged in successfully",
                "data": [{
                    "access_token": create_access_token(data["email"]),
                    "is_admin": False
                }]}

        return response, 200
