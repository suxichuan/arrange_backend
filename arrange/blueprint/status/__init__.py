from flask import Blueprint
from flask_restful import Api



status_blueprint=Blueprint("status",__name__,url_prefix="/status")
status_api=Api(status_blueprint)

from . import views