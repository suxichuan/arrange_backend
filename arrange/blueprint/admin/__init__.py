from flask import Blueprint
from flask_restful import Api



admin_blueprint=Blueprint("admin",__name__,url_prefix="/admin")
admin_api=Api(admin_blueprint)

from . import views