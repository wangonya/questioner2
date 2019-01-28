from flask import Flask, Blueprint, jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager

from config import APP_CONFIG
from .db import InitDb
from .auth.signup import Signup
from .auth.login import Login
from .meetups.meetups import PostMeetups, Meetups, GetSpecificMeetup
from .questions.post_questions import PostQuestion
from .questions.vote import Upvote, Downvote
from .meetups.rsvps import Rsvp
from .questions.comment import Comment
from .meetups.delete import DeleteMeetup
from .utils.error_handlers import errors


def create_app(default_config):
    """create app factory"""
    app = Flask(__name__)
    app.config.from_object(APP_CONFIG[default_config])
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp, errors=errors)
    JWTManager(app)
    app.config['JWT_SECRET_KEY'] = 'questioner-jwt-secret'

    app.register_blueprint(api_bp, url_prefix='/api/v2')

    @app.errorhandler(404)
    def page_not_found(e):
        response = jsonify({'status': 404, 'message': 'The url you requested for was not found'})
        response.status_code = 404
        return response

    @app.errorhandler(500)
    def page_not_found(e):
        response = jsonify({'status': 404, 'message': 'Something went wrong. Please try again later'})
        response.status_code = 500
        return response

    class HelloWorld(Resource):
        """Project root route -- just shows hello world for testing"""
        @staticmethod
        def get():
            """test get -- just shows hello world for testing"""
            return "Hello World!"

    api.add_resource(HelloWorld, '/', strict_slashes=False)
    api.add_resource(Signup, '/auth/signup', strict_slashes=False)
    api.add_resource(Login, '/auth/login', strict_slashes=False)
    api.add_resource(PostMeetups, '/meetups', strict_slashes=False)
    api.add_resource(Meetups, '/meetups/upcoming', strict_slashes=False)
    api.add_resource(GetSpecificMeetup, '/meetups/<int:m_id>', strict_slashes=False)
    api.add_resource(PostQuestion, '/meetups/<int:m_id>/questions', strict_slashes=False)
    api.add_resource(Upvote, '/questions/<int:q_id>/upvote', strict_slashes=False)
    api.add_resource(Downvote, '/questions/<int:q_id>/downvote', strict_slashes=False)
    api.add_resource(Rsvp, '/meetups/<int:m_id>/rsvps', strict_slashes=False)
    api.add_resource(Comment, '/comments/<int:q_id>', strict_slashes=False)
    api.add_resource(DeleteMeetup, '/meetups/<int:m_id>', strict_slashes=False)

    return app
