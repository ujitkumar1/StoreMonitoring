import os

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from app.celery_system import make_celery

app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/1',
    result_backend='redis://localhost:6379/2'
)

# Database Setup
app.secret_key = "ujit1"
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'db.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

celery = make_celery(app)
db = SQLAlchemy(app)
api = Api(app)
