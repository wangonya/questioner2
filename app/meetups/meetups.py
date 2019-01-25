import json

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..meetups.models import MeetupModel
from ..auth.models import AuthModel
from ..utils.validators import MeetupValidators, GeneralValidators
from ..utils.error_handlers import NoDataError


class Meetups(Resource):
    """upcoming meetups endpoint resource"""
    parser = reqparse.RequestParser()
    parser.add_argument("title",
                        type=GeneralValidators.non_empty_string,
                        required=True,
                        nullable=False,)
    parser.add_argument("location",
                        type=GeneralValidators.non_empty_string,
                        required=True,
                        nullable=False,)
    parser.add_argument("happening_on",
                        type=GeneralValidators.non_empty_string,
                        required=True,
                        nullable=False,)
    parser.add_argument("image",
                        type=str)
    parser.add_argument("tags", action="append")

    @staticmethod
    def get():
        """do a GET to upcoming meetups endpoint"""
        meetups = MeetupModel.get_upcoming_meetups()
        meetups = json.dumps(meetups, default=str)

        if len(json.loads(meetups)) < 1:
            raise NoDataError

        return {"status": 200,
                "data": json.loads(meetups)}, 200


class PostMeetups(Resource):
    """post new meetup endpoint"""

    @staticmethod
    @jwt_required
    def post():
        """do a POST to the meetups endpoint"""
        data = Meetups.parser.parse_args()

        user = get_jwt_identity()
        creator = AuthModel.find_by_email(user)
        MeetupValidators.check_creator_is_admin(creator)

        title = data["title"]
        creator_id = creator["id"]
        location = data["location"]
        happening_on = data["happening_on"]
        tags = data["tags"]
        image = data["image"]

        MeetupValidators.check_duplicate_meetup(title)

        meetup = MeetupModel(title, creator_id, location,
                             happening_on, tags, image)
        meetup.save_meetup_to_db()

        response = {
            "status": 201,
            "message": "meetup created successfully",
            "data": [{
                "title": title,
                "location": location,
                "happeningOn": happening_on,
                "tags": tags,
            }]}

        return response, 201


class GetSpecificMeetup(Resource):
    @staticmethod
    def get(m_id):
        """send a GET to the specific meetup endpoint"""
        MeetupValidators.check_meetup_exists(m_id)

        meetup = MeetupModel.get_specific_meetup(m_id)
        meetup = json.dumps(meetup, default=str)

        response = {
            "status": 200,
            "data": json.loads(meetup)
        }

        return response, 200
