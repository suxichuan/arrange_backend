from flask import Blueprint
from flask_restful import Api

duty_blueprint=Blueprint('duty_blueprint',__name__,url_prefix='/duty')
duty_api=Api(duty_blueprint)

from . import view