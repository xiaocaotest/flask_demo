import os
import sys

import logging
from flask import Flask

from src.base.config.config import *
from src.base.utils.database import db
import src.base.utils.responses as resp
from flask_jwt_extended import JWTManager
from src.base.api.books import book_routes
from src.base.api.users import user_routes
from src.base.api.authors import author_routes
from src.base.utils.responses import response_with


if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

app = Flask(__name__)
app.config.from_object(app_config)

app.register_blueprint(book_routes, url_prefix='/api/books')
app.register_blueprint(user_routes, url_prefix='/api/users')
app.register_blueprint(author_routes, url_prefix='/api/authors')


@app.after_request
def add_header(response):
    return response


@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)


@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)


@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


jwt = JWTManager(app)

db.init_app(app)

with app.app_context():
    db.create_all()

logging.basicConfig(
        stream=sys.stdout,
        format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)s|%(message)s',
        level=logging.DEBUG)