
from . import role_blueprint,role_api
from arrange.models.roleModel import role_model
from flask_cors import cross_origin
from flask import jsonify,request
from arrange.utils.code import to_dict_code
from flask_restful import Resource


roleModel=role_model()

class role(Resource):
    def get(self):
        rolelist=roleModel.get_list()
        if len(rolelist)>0:
            ls=[]
            for row in rolelist:
                 ls.append({'role_id':row[0],'role_name':row[1]})
            return jsonify(to_dict_code('20000', data=ls))
        else:
            return jsonify(to_dict_code('20001', data=None))
    def post(self):
       pass
role_api.add_resource(role,'/rolelist')


@role_blueprint.route('/add',methods=['post'])
@cross_origin()
def add_role():
    role_name = request.form.get("role_name")
    res=roleModel.add_role(role_name)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))


@role_blueprint.route('/delete',methods=['get'])
@cross_origin()
def delete_role_by_id():
    role_id = request.args.get("role_id")
    res=roleModel.delete_role_by_id(role_id)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))

@role_blueprint.route('/update',methods=['post'])
@cross_origin()
def update_role_by_id():
    role_id = request.form.get("role_id")
    role_name = request.form.get("role_name")
    res=roleModel.update_role_by_id(role_id,role_name)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))


@role_blueprint.route("/list", methods=['get'])
@cross_origin()
def get_role_list():
    current_page = int(request.args.get("current_page"))
    page_size = int(request.args.get("page_size"))
    keyword = request.args.get("keyword")
    if keyword == 'null':
        keyword = None
    if current_page < 1:
        current_page = 1
    offset = (current_page - 1) * page_size
    res = roleModel.get_role_list(offset,page_size,keyword)
    role_list = res[0]
    role_ls = []
    for role in role_list:
        r = role.serialization()
        role_ls.append(r)
    total = int(res[1])
    if total % page_size == 0:
        total_page = int(total / page_size)
    else:
        total_page = int(total / page_size) + 1
    data = {
        'page':
            {
                'current_page': current_page,
                'page_size': page_size,
                'total': total,
                'total_page': total_page,
                'list': role_ls
            }
    }
    return jsonify(to_dict_code('20000', data=data))


@role_blueprint.route("/updatestatus",methods=['post'])
@cross_origin()
def update_role_status():
    global update_status
    role_id=request.form.get("role_id")
    role_isdisable = request.form.get("role_isdisable")
    if role_isdisable=='1':
        update_status='0'
    if role_isdisable=='0':
        update_status='1'
    res=roleModel.updatestatus(role_id,update_status)
    if res==1:
        return jsonify(to_dict_code('20004',data=None))
    return jsonify(to_dict_code('20005',data=None))