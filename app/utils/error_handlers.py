from werkzeug.exceptions import HTTPException


class DatabaseConnectionError(HTTPException):
    """handle database connection error"""
    code = 500
    description = "An error occurred while connecting to the database"


class TableCreationError(HTTPException):
    """handle table creation error"""
    code = 500
    description = "An error occurred while creating the tables"


class InvalidEmailFormatError(HTTPException):
    """handle invalid email format"""
    code = 400
    description = "Invalid email format"


class UserAlreadyExistsError(HTTPException):
    """handle duplicate user registration"""
    code = 409
    description = "A user with that email already exists"


class InvalidPasswordLengthError(HTTPException):
    """handle duplicate user registration"""
    code = 400
    description = "Password length has to be at least 6 characters"


class UserLoginError(HTTPException):
    """handle invalid login details"""
    code = 401
    description = "Invalid login details provided"


class DuplicateDataError(HTTPException):
    """handle duplicate data entries"""
    code = 409
    description = "The entered data already exists"


class AdminProtectedError(HTTPException):
    """handle admin protected routes"""
    code = 401
    description = "Only an admin user can access this endpoint"


class NoDataError(HTTPException):
    """handle missing data requested"""
    code = 404
    description = "The data you requested for does not exist"
