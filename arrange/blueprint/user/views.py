from . import user_blueprint,user_Api
from arrange.models import user
from flask import request
from flask_restful import Resource
from arrange.models.user_model import usermodel,user
class user(Resource):
    def get(self):
        pass
    def post(self):
        pass

user_Api.add_resource(user,"/adduser")

@user_blueprint.route("/")
def user_index():
    return "hello user"


@user_blueprint.route("/regist",methods=['post'])
def regist():

    username=request.args.get("username")
    password=request.args.get("password")
    email=request.args.get("email")
    nickname=request.args.get("nackname")
    phone=request.args.get("phone")
    usr = user()
    usr.username=username
    usr.password=password
    usr.nickname=nickname
    usr.email=email
    usr.phone=phone
    usermodel().add_user(usr)
    return 'ok'

@user_blueprint.route("/login",methods=['get'])
def login():
    username=request.args.get("username")
    password=request.args.get("password")
    if all(username,password):
        pass
    return 'ok'