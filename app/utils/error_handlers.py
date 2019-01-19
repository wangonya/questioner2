from werkzeug.exceptions import HTTPException


class DatabaseConnectionError(HTTPException):
    """handle database connection error"""
    code = 500
    description = "An error occurred while connecting to the database"


class TableCreationError(HTTPException):
    """handle database connection error"""
    code = 500
    description = "An error occurred while creating the tables"
