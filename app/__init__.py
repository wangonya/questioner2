from datetime import timedelta
from flask import Flask, Blueprint, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger

from config import APP_CONFIG
from .db import InitDb
from .auth.signup import Signup
from .auth.login import Login
from .meetups.meetups import PostMeetups, Meetups, GetSpecificMeetup, GetSpecificMeetupQuestion
from .questions.post_questions import PostQuestion
from .questions.vote import Upvote, Downvote
from .meetups.rsvps import Rsvp
from .questions.comment import Comment
from .meetups.delete import DeleteMeetup
from .utils.error_handlers import errors
from .auth.profile import UserProfile, AdminProfile


def create_app(default_config):
    """create app factory"""
    app = Flask(__name__)
    app.config.from_object(APP_CONFIG[default_config])
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp, errors=errors)
    jwt = JWTManager(app)
    app.config['JWT_SECRET_KEY'] = 'questioner-jwt-secret'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
    app.config['SWAGGER'] = {'title': 'Questioner', 'uiversion': 3}
    CORS(app)

    app.register_blueprint(api_bp, url_prefix='/api/v2')

    @app.errorhandler(404)
    def page_not_found(e):
        """custom 404 handler"""
        response = jsonify({'status': 404, 'message': 'The url you requested for was not found'})
        response.status_code = 404
        return response

    @jwt.expired_token_loader
    def my_expired_token_callback():
        """custom token expired message"""
        return jsonify({
            'status': 401,
            'message': 'Your access token has expired'
        }), 401

    class HelloWorld(Resource):
        """Project root route -- just shows hello world for testing"""
        @staticmethod
        def get():
            """test get -- just shows hello world for testing"""
            return "Hello World!"

    template = {
        "swagger": "3.0",
        "info": {
            "title": "Questioner",
            "description": "Crowd-source questions for a meetup. Questioner helps the meetup organizer prioritize "
                           "questions to be answered. Other users can vote on asked questions and they bubble to the "
                           "top or bottom of the log.",
            "version": "2.0",
            "email": "kwangonya@gmail.com",
            "url": "wangonya.com",
        },
        "host": "questioner2.herokuapp.com",
        "schemes": [
            "https"
        ]
    }

    Swagger(app, template=template)

    api.add_resource(HelloWorld, '/', strict_slashes=False)
    api.add_resource(Signup, '/auth/signup', strict_slashes=False)
    api.add_resource(Login, '/auth/login', strict_slashes=False)
    api.add_resource(PostMeetups, '/meetups', strict_slashes=False)
    api.add_resource(Meetups, '/meetups/upcoming', strict_slashes=False)
    api.add_resource(GetSpecificMeetup, '/meetups/<int:m_id>', strict_slashes=False)
    api.add_resource(GetSpecificMeetupQuestion, '/questions/<int:q_id>', strict_slashes=False)
    api.add_resource(PostQuestion, '/meetups/<int:m_id>/questions', strict_slashes=False)
    api.add_resource(Upvote, '/questions/<int:q_id>/upvote', strict_slashes=False)
    api.add_resource(Downvote, '/questions/<int:q_id>/downvote', strict_slashes=False)
    api.add_resource(Rsvp, '/meetups/<int:m_id>/rsvps', strict_slashes=False)
    api.add_resource(Comment, '/comments/<int:q_id>', strict_slashes=False)
    api.add_resource(DeleteMeetup, '/meetups/<int:m_id>', strict_slashes=False)
    api.add_resource(UserProfile, '/profile', strict_slashes=False)
    api.add_resource(AdminProfile, '/admin', strict_slashes=False)

    return app
