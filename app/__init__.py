from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_marshmallow import Marshmallow


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super secret key'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Applications/Python3.7/Scripts/VisualBi/app/jobportal.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'jobportal.db')
db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config.from_object(__name__)
from app import views