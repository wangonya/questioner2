from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..meetups.models import MeetupModel
from ..auth.models import AuthModel
from ..utils.validators import MeetupValidators


class Meetups(Resource):
    """upcoming meetups endpoint resource"""
    parser = reqparse.RequestParser()
    parser.add_argument("title",
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument("location",
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument("happening_on",
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument("image",
                        type=str)
    parser.add_argument("tags", action="append")


class PostMeetups(Resource):
    """post new meetup endpoint"""
    @jwt_required
    def post(self):
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
            "status": 200,
            "message": "meetup created successfully",
            "data": [{
                "title": title,
                "location": location,
                "happeningOn": happening_on,
                "tags": tags,
            }]}

        return response, 201
