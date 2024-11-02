import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'  # Use environment variable or fallback
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'  # Use environment variable for DB URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
