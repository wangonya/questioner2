from app.db import InitDb


class InsertDataToDb:
    """reusable methods for inserting data to db"""

    @staticmethod
    def save_data_to_db(table, *args):
        """save entered data to db"""
        insert_query = ('INSERT INTO {} '
                        '({},{},{},{},{},{}) '
                        'VALUES (%s, %s, %s, %s, %s, %s);'
                        .format(table, args[0], args[1], args[2],
                                args[3], args[4], args[5]))
        InitDb.cursor.execute(insert_query,
                              (args[6], args[7], args[8],
                               args[9], args[10], args[11]))
