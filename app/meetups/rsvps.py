from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..meetups.models import RsvpsModel
from ..utils.validators import (RsvpValidators, MeetupValidators,
                                GeneralValidators)
from ..db.select import SelectDataFromDb


class Rsvp(Resource):
    """resource for Rsvp endpoint"""
    parser = reqparse.RequestParser()
    parser.add_argument("status",
                        type=str,
                        required=True,
                        nullable=False,)

    @jwt_required
    def post(self, m_id):
        """do POST on rsvp endpoint"""
        data = self.parser.parse_args()
        status = data["status"]
        user = get_jwt_identity()
        userid = SelectDataFromDb.conditional_where_select("users", "email", user)

        GeneralValidators.non_empty_string(**data)
        MeetupValidators.check_meetup_exists(m_id)
        RsvpValidators.check_proper_rsvp(status)

        rsvp = RsvpsModel(status, userid, m_id)
        if not RsvpsModel.check_duplicate_rsvp(userid, m_id):
            rsvp.save_rsvp_to_db()
            response = {
                "status": 201,
                "msg": "meetup rsvp successful",
                "data": [{
                    "m_id": m_id,
                    "status": status.lower()
                }]
            }
            return response, 201
        else:
            RsvpsModel.update_rsvp(status, userid, m_id)
            response = {
                "status": 200,
                "msg": "meetup rsvp update successful",
                "data": [{
                    "m_id": m_id,
                    "status": status.lower()
                }]
            }
            return response, 200
