import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    ADMIN_TOKEN = os.environ["ADMIN_TOKEN"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = True