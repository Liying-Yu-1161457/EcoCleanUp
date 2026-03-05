from flask import g
import psycopg2
import psycopg2.extras

# database connection settings
connection_params = {}

def init_db(app, user, password, host, database, port=5432, autocommit=True):
    """setup database connection for the app"""
    connection_params['user'] = user
    connection_params['password'] = password
    connection_params['host'] = host
    connection_params['database'] = database
    connection_params['port'] = port
    connection_params['autocommit'] = autocommit

    # close db when app context ends
    app.teardown_appcontext(close_db)

def get_db():
    """get database connection for current request"""
    if 'db' not in g:
        conn = psycopg2.connect(
            user=connection_params['user'],
            password=connection_params['password'],
            host=connection_params['host'],
            dbname=connection_params['database'],
            port=connection_params['port']
        )
        conn.autocommit = connection_params.get('autocommit', True)
        g.db = conn
    return g.db

def get_cursor():
    """get database cursor for current request"""
    return get_db().cursor(cursor_factory=psycopg2.extras.RealDictCursor)

def close_db(exception=None):
    """close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()