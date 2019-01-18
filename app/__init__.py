from flask import Flask, Blueprint
from flask_restful import Api, Resource

from config import APP_CONFIG
from .utils.error_handlers import ERRORS


def create_app(default_config):
    """create app factory"""
    app = Flask(__name__)
    app.config.from_object(APP_CONFIG[default_config])
    api_bp = Blueprint('api', __name__)
    api = Api(api_bp, errors=ERRORS)

    # register blueprint
    app.register_blueprint(api_bp, url_prefix='/api/v2')

    class HelloWorld(Resource):
        """Project root route -- just shows hello world for testing"""
        @staticmethod
        def get():
            """test get -- just shows hello world for testing"""
            return "Hello World!"

    # register routes
    api.add_resource(HelloWorld, '/')

    return app
