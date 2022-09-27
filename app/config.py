from dotenv import load_dotenv
import os
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    COUCHBASE_DB_HOST = os.getenv("COUCHBASE_DB_HOST")
    COUCHBASE_USERNAME = os.getenv("COUCHBASE_USERNAME")
    COUCHBASE_PASSWORD = os.getenv("COUCHBASE_PASSWORD")
    COUCHBASE_BUCKET = os.getenv("COUCHBASE_BUCKET")
    PORT = os.getenv("PORT", 5000)


class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY")


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    HOST = 'localhost'

class TestingConfig(Config):
    TESTING = True
