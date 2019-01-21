import psycopg2

from .error_handlers import (DatabaseConnectionError, TableCreationError)


class DbValidators:
    """database operation validators"""
    @staticmethod
    def connect_to_db(db_uri):
        """try making a connection to the db"""
        try:
            cnxn = psycopg2.connect(db_uri)
            print("Connection successful")
            return cnxn
        except (Exception, psycopg2.Error):
            raise DatabaseConnectionError

    @staticmethod
    def create_tables(cnxn, cursor, *tables):
        """create db tables"""
        try:
            for table in tables:
                cursor.execute(table)
                cnxn.commit()
            print("Tables created successfully")
        except (Exception, psycopg2.Error):
            raise TableCreationError
        finally:
            # close the database connection.
            if cnxn:
                cursor.close()
                cnxn.close()
