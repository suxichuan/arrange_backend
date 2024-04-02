from flask import Blueprint
from flask_restful import Api
staff_blueprint=Blueprint('staff',__name__,url_prefix="/staff")
staff_api=Api(staff_blueprint)
from . import views