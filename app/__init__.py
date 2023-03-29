from flask import Flask
from flask.cli import FlaskGroup
# import logging


# logging.basicConfig(filename='logs.log', level=logging.DEBUG)

app = Flask(__name__)

app.config.from_object('config')

manager = FlaskGroup(app)


from app.controllers import default
from app.controllers import bitrix24
from app.exceptions import exceptions
