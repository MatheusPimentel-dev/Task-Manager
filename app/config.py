import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False