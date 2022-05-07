import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from dotenv import load_dotenv

# load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SECRET_KEY = os.urandom(32)

app = Flask(__name__, static_folder='static')

# Local DB Environment
# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shop.db')

# Remote DB Environment
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://c21024669:Rotate-Cow18@csmysql.cs.cf.ac.uk:3306/c21024669_deltaverse'

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

from shop import routes
