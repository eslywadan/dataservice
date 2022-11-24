import pandas as pd


def read_query(query, connection):
    """ query is the sql str passing for the query engine
    the connection is connection gen by dbtool.db_connection """

    cursor = connection.cursor()
    try:
        cursor.execute( query )
        names = [ x[0] for x in cursor.description]
        rows = cursor.fetchall()
        return pd.DataFrame( rows, columns=names)
    finally:
        if cursor is not None:
            cursor.close()