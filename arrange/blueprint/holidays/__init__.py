from flask import Blueprint
from flask_restful import Api

special_holidays=Blueprint("holidays",__name__,url_prefix="/holidays")
special_holidays_api=Api(special_holidays)

from . import views