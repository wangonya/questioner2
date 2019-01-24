from flask import Flask, Blueprint
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager

from config import APP_CONFIG
from .db import CreateTables
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

    class HelloWorld(Resource):
        """Project root route -- just shows hello world for testing"""
        @staticmethod
        def get():
            """test get -- just shows hello world for testing"""
            return "Hello World!"

    api.add_resource(HelloWorld, '/')
    api.add_resource(Signup, '/auth/signup')
    api.add_resource(Login, '/auth/login')
    api.add_resource(PostMeetups, '/meetups')
    api.add_resource(Meetups, '/meetups/upcoming')
    api.add_resource(GetSpecificMeetup, '/meetups/<int:m_id>')
    api.add_resource(PostQuestion, '/meetups/<int:m_id>/questions')
    api.add_resource(Upvote, '/questions/<int:q_id>/upvote')
    api.add_resource(Downvote, '/questions/<int:q_id>/downvote')
    api.add_resource(Rsvp, '/meetups/<int:m_id>/rsvps')
    api.add_resource(Comment, '/comments/<int:q_id>')
    api.add_resource(DeleteMeetup, '/meetups/<int:m_id>')

    return app
