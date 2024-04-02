from flask import Blueprint
from flask_restful import Api

place_blueprint=Blueprint("place",__name__,url_prefix="/place")
place_api=Api(place_blueprint)

from . import views