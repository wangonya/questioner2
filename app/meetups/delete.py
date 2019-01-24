from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..meetups.models import MeetupModel
from ..auth.models import AuthModel
from ..utils.error_handlers import DeleteProtectedError
from ..utils.validators import MeetupValidators


class DeleteMeetup(Resource):
    """delete meetup"""
    @staticmethod
    @jwt_required
    def delete(m_id):
        user = get_jwt_identity()
        userid = AuthModel.find_by_email(user)
        meetup = MeetupModel.get_specific_meetup(m_id)

        MeetupValidators.check_meetup_exists(m_id)

        if not userid["id"] == meetup[0]["creator"]:
            raise DeleteProtectedError
        else:
            MeetupModel.delete_meetup(m_id)
            return {"status": 200, "data": ["Delete successful"]}, 200
