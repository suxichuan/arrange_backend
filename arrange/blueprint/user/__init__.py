from flask import Blueprint
from flask_restful import Api
user_blueprint=Blueprint('user',__name__,url_prefix="/user")
user_Api=Api(user_blueprint)
from . import views