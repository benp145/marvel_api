from dotenv import load_dotenv
import os

# Specify the file location for current directory
basedir = os.path.abspath(os.path.dirname(__name__))
# load the environment variables from .env file
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    FLASK_APP = os.getenv('FLASK_APP')
    FLASK_ENV = os.getenv('FLASK_ENV')
    if os.getenv('SQLALCHEMY_DATABASE_URI').startswith('postgres'):
        SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI').replace('postgres','postgresql')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    SECRET_KEY = os.getenv('SECRET_KEY')