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
        """
        RSVP Meetup
        ---
            tags:
            - meetups
            consumes:
            - application/json
            parameters:
            - in: header
              name: Authorization
              description: JWT token
              type: string
              required: true
            - in: path
              name: m_id
              type: int
              required: true
              description: The id of the meetup to rsvp
            - in: body
              name: RSVP meetup
              description: Rsvp for a meetup
              schema:
                id: RSVP Meetup
                type: object
                required:
                - status
                properties:
                  status:
                    type: string
            responses:
              201:
                description: meetup rsvp successful
              200:
                description: meetup rsvp update successful
              400:
                description: Rsvp status can only be 'yes', 'no' or 'maybe'
              404:
                description: No meetup matching the id passed was found
        """
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
                "message": "meetup rsvp successful",
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
                "message": "meetup rsvp update successful",
                "data": [{
                    "m_id": m_id,
                    "status": status.lower()
                }]
            }
            return response, 200
