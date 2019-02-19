import json

from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..meetups.models import MeetupModel
from ..utils.validators import MeetupValidators, GeneralValidators
from ..utils.error_handlers import NoDataError
from ..db.select import SelectDataFromDb


class Meetups(Resource):
    """upcoming meetups endpoint resource"""
    parser = reqparse.RequestParser()
    parser.add_argument("title",
                        type=str,
                        required=True,
                        nullable=False,)
    parser.add_argument("details",
                        type=str,
                        required=True,
                        nullable=False, )
    parser.add_argument("location",
                        type=str,
                        required=True,
                        nullable=False,)
    parser.add_argument("happening_on",
                        type=str,
                        required=True,
                        nullable=False,)
    parser.add_argument("image",
                        type=str)
    parser.add_argument("tags",
                        type=str)

    @staticmethod
    def get():
        """
        GET Upcoming Meetups
        ---
        tags:
        - meetups
        responses:
          200:
            description: OK
          404:
            description: The data you requested for was not found
        """
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
        """
        Post Meetup
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
            - in: body
              name: Create meetup
              description: Create new meetup
              schema:
                id: Post Meetup
                type: object
                required:
                - title
                - details
                - location
                - happening_on
                - image
                - tags
                properties:
                  title:
                    type: string
                  details:
                    type: string
                  location:
                    type: string
                  happening_on:
                    type: string
                  image:
                    type: string
                  tags:
                    type: string
            responses:
              201:
                description: meetup created successfully
              400:
                description: Invalid data format
              401:
                description: Only an admin can create a meetup
        """
        data = Meetups.parser.parse_args()

        GeneralValidators.non_empty_string(**data)
        GeneralValidators.date_format(data["happening_on"])

        user = get_jwt_identity()
        creator = SelectDataFromDb.conditional_where_select("users", "email", user)
        MeetupValidators.check_creator_is_admin(creator)

        title = data["title"]
        details = data["details"]
        creator_id = creator["id"]
        location = data["location"]
        happening_on = data["happening_on"]
        tags = data["tags"]
        image = data["image"]

        MeetupValidators.check_duplicate_meetup(title, happening_on)

        meetup = MeetupModel(title, details, creator_id, location,
                             happening_on, tags, image)
        meetup.save_meetup_to_db()

        response = {
            "status": 201,
            "message": "meetup created successfully",
            "data": [{
                "title": title,
                "details": details,
                "location": location,
                "happeningOn": happening_on,
                "tags": tags,
            }]}

        return response, 201


class GetSpecificMeetup(Resource):
    """get specific meetup"""
    @staticmethod
    def get(m_id):
        """
        GET Specific Meetup
        ---
        tags:
        - meetups
        parameters:
        - in: path
          name: m_id
          type: int
          required: true
          description: The id of the meetup to view
        responses:
          200:
            description: OK
          404:
            description: No meetup matching the id passed was found
        """
        MeetupValidators.check_meetup_exists(m_id)

        meetup = MeetupModel.get_specific_meetup(m_id)
        meetup = json.dumps(meetup, default=str)

        response = {
            "status": 200,
            "data": json.loads(meetup)
        }

        return response, 200


class GetSpecificMeetupQuestion(Resource):
    """get specific meetup question"""
    @staticmethod
    def get(q_id):
        """send a GET to the specific meetup endpoint"""

        question = MeetupModel.get_specific_meetup_question(q_id)
        question = json.dumps(question, default=str)

        response = {
            "status": 200,
            "data": json.loads(question)
        }

        return response, 200
