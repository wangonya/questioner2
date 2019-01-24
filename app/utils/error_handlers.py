from werkzeug.exceptions import HTTPException


class DatabaseConnectionError(HTTPException):
    """handle database connection error"""
    status = 500


class TableCreationError(HTTPException):
    """handle table creation error"""


class InvalidEmailFormatError(HTTPException):
    """handle invalid email format"""


class UserAlreadyExistsError(HTTPException):
    """handle duplicate user registration"""


class InvalidPasswordLengthError(HTTPException):
    """handle duplicate user registration"""


class UserLoginError(HTTPException):
    """handle invalid login details"""


class DuplicateDataError(HTTPException):
    """handle duplicate data entries"""


class AdminProtectedError(HTTPException):
    """handle admin protected routes"""


class DeleteProtectedError(HTTPException):
    """handle meetup deletion to make sure only the admin that created the
    meetup can delete it"""


class NoDataError(HTTPException):
    """handle missing data requested"""


class InvalidRsvpStatusError(HTTPException):
    """handle invalid rsvp status"""


class MeetupIdDoesNotExist(HTTPException):
    """handle missing meetup"""


class QuestionIdDoesNotExist(HTTPException):
    """handle missing question"""


errors = {
    "UserAlreadyExistsError": {
        "message": "A user with that email already exists",
        "status": 409,
    },
    "InvalidEmailFormatError": {
        "message": "Invalid email format",
        "status": 400,
    },
    "InvalidPasswordLengthError": {
        "message": "Password length has to be at least 6 characters",
        "status": 400,
    },
    "UserLoginError": {
        "message": "Incorrect login details provided",
        "status": 401,
    },
    "NoDataError": {
        "message": "The data you requested for was not found",
        "status": 404,
    },
    "AdminProtectedError": {
        "message": "Only an admin user can access this endpoint",
        "status": 401,
    },
    "DuplicateDataError": {
        "message": "The data provided already exists in the resource",
        "status": 409,
    },
    "InvalidRsvpStatusError": {
        "message": "Rsvp status can only be 'yes', 'no' or 'maybe'",
        "status": 400,
    },
    "DatabaseConnectionError": {
        "message": "An error occurred while connecting to the database",
        "status": 500,
    },
    "TableCreationError": {
        "message": "An error occurred while creating the tables",
        "status": 500,
    },
    "DeleteProtectedError": {
        "message": "Only the admin that created this endpoint can delete it",
        "status": 401,
    },
    "MeetupIdDoesNotExist": {
        "message": "No meetup matching the id passed was found",
        "status": 404,
    },
    "QuestionIdDoesNotExist": {
        "message": "No question matching the id passed was found",
        "status": 404,
    }
}
