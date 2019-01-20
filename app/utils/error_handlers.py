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
