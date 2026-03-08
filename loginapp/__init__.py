from flask import Flask
from datetime import datetime
import os

# get root path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# point to root static path
app = Flask(__name__,
            static_folder=os.path.join(root_dir, 'static'),
            static_url_path='/static')

app.secret_key = 'Example Secret Key (CHANGE THIS TO YOUR OWN SECRET KEY!)'

# Set up database connection.
from loginapp import connect
from loginapp import db
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname,
           connect.dbport)

@app.context_processor
def utility_processor():
    return {'now': datetime.now}

from loginapp import user
from loginapp import volunteer
from loginapp import event_leader
from loginapp import admin