from flask import Flask
from flask_cors import CORS
import os

from app.couchbase_client import CouchbaseClient


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    db_info = {
        "host": app.config['COUCHBASE_DB_HOST'],
        "bucket": app.config['COUCHBASE_BUCKET'],
        "username": app.config['COUCHBASE_USERNAME'],
        "password": app.config['COUCHBASE_PASSWORD'],
    }
    cb = CouchbaseClient(*db_info.values())
    cb.connect()
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization,x-api-key"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,OPTION,PUT,POST,DELETE"
        )
        return response

    @app.route("/")
    def start_page():
        """Function to load the splash screen mainly for gitpod demo as the initialization takes time4"""
        return 'Supplier API'
    return app
