from app.db import InitDb


class SelectDataFromDb:
    """reusable methods of selecting data from db"""

    @staticmethod
    def general_select(table):
        """helper function for general selection (*)"""
        InitDb.cursor.execute('SELECT * FROM {}'.format(table))
        data = InitDb.cursor.fetchall()
        return data

    @staticmethod
    def conditional_where_select(table, column, data):
        """helper function for conditional where selection"""
        query = ('SELECT * FROM {} WHERE {} = %s'
                 .format(table, column))
        InitDb.cursor.execute(query, (data,))
        data = InitDb.cursor.fetchone()
        return data

    @staticmethod
    def conditional_where_and_select(table, *args):
        """helper function for conditional where selection"""
        query = ('SELECT * FROM {} '
                 'WHERE {} = %s '
                 'AND {} = %s'.format(table, args[0], args[2]))
        InitDb.cursor.execute(query, (args[1], args[3]))
        data = InitDb.cursor.fetchone()
        return data
