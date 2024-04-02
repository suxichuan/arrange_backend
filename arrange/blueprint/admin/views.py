from arrange.blueprint.admin import admin_blueprint,admin_api
from arrange.models.adminModel import admin_model,admin
from flask import request,jsonify,make_response
from flask_restful import Resource
from arrange.utils.code import  to_dict_code
from flask_cors import cross_origin
from arrange.utils.token import generate_auth_token
import re

admin_Model=admin_model()

class admin(Resource):
    def get(self):
        pass

    def post(self):
        account=request.form.get("account")
        passwd=request.form.get("passwd")
        # admin_Model = admin_model()
        if account is None or len(account)<6:
            return jsonify(to_dict_code('10001',data=None))
        if passwd is None or len(passwd)<6:
            return jsonify(to_dict_code('10002'))
        if all([account,passwd]):
            adm=admin_Model.check_exist(account)
            if adm:
               return jsonify(to_dict_code('10000',data=None))
        name=request.form.get("name")
        nickname=request.form.get("nickname")
        email=request.form.get("email")
        email_patten=r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'
        if not re.match(email_patten,email):
            return jsonify(to_dict_code('10003',data=None))
        telephone = request.form.get("telephone")
        telephone_patten=r'^1[3-9]\d{9}$'
        if not re.match(telephone_patten,str(telephone)):
            return jsonify(to_dict_code('10004', data=None))
        Admin=admin()
        Admin.password=passwd
        Admin.account=account
        Admin.name=name
        Admin.nickname=nickname
        Admin.email=email
        Admin.telephone=telephone
        res=admin_Model.add_admin(Admin)
        if res:
            return jsonify(to_dict_code('20001',data=None))
        else:
            return jsonify(to_dict_code('20002',data=None))



admin_api.add_resource(admin,"/addadmin")

@admin_blueprint.route("/login",methods=['post'])
@cross_origin()
def adminLogin():
    account=request.form.get('username')
    password=request.form.get('password')
    if all([account,password]):
       adminobj=admin_Model.find_admin_by_account(account)
       if adminobj:
            if adminobj.check_passwd(password):
                token=generate_auth_token({'adminid':adminobj.account})
                resp = make_response(to_dict_code('20003',data={'token':token}))
                return resp
    return jsonify(to_dict_code('10007',data=None))
