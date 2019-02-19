from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..meetups.models import MeetupModel
from ..utils.error_handlers import DeleteProtectedError
from ..utils.validators import MeetupValidators
from ..db.select import SelectDataFromDb


class DeleteMeetup(Resource):
    """delete meetup"""
    @staticmethod
    @jwt_required
    def delete(m_id):
        """
        DELETE Specific Meetup
        ---
        tags:
        - meetups
        parameters:
        - in: path
          name: m_id
          type: int
          required: true
          description: The id of the meetup to delete
        responses:
          200:
            description: OK
          401:
            description: Only the admin that created this meetup can delete it
          404:
            description: No meetup matching the id passed was found
        """
        user = get_jwt_identity()
        userid = SelectDataFromDb.conditional_where_select("users", "email", user)
        meetup = MeetupModel.get_specific_meetup(m_id)

        MeetupValidators.check_meetup_exists(m_id)

        if userid["id"] != meetup[0]["creator"]:
            raise DeleteProtectedError
        else:
            MeetupModel.delete_meetup(m_id)
            return {"status": 200, "data": [{"message": "Delete successful"}]}, 200
