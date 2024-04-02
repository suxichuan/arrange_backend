
from . import status_blueprint,status_api
from arrange.models.statusModel import status_model
from flask_cors import cross_origin
from flask import jsonify,request
from arrange.utils.code import to_dict_code
from flask_restful import Resource


status_Model=status_model()

class status(Resource):
    def get(self):
        statuslist=status_Model.get_list()
        if len(statuslist)>0:
            ls=[]
            for row in statuslist:
                 ls.append({'status_id':row[0],'status_name':row[1]})
            return jsonify(to_dict_code('20000', data=ls))
        else:
            return jsonify(to_dict_code('20001', data=None))
    def post(self):
       pass
status_api.add_resource(status,'/statuslist')

@status_blueprint.route("/list",methods=['get'])
@cross_origin()
def get_status_list():
    current_page = int(request.args.get("current_page"))
    page_size = int(request.args.get("page_size"))
    keyword = request.args.get("keyword")
    if keyword == 'null':
        keyword = None
    if current_page < 1:
        current_page = 1
    offset = (current_page - 1) * page_size
    res = status_Model.get_status_lists(offset, page_size, keyword)
    status_list = res[0]
    status_ls = []
    for status in status_list:
        r = status.serialization()
        status_ls.append(r)
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
                'list': status_ls
            }
    }
    return jsonify(to_dict_code('20000', data=data))


@status_blueprint.route('/update',methods=['post'])
@cross_origin()
def update_status_by_id():
    status_id = request.form.get("status_id")
    status_name = request.form.get("status_name")
    res=status_Model.update_status_by_id(status_id,status_name)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))


@status_blueprint.route('/delete',methods=['get'])
@cross_origin()
def delete_status_by_id():
    status_id = request.args.get("status_id")
    res=status_Model.delete_status_by_id(status_id)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))


@status_blueprint.route('/add',methods=['post'])
@cross_origin()
def add_status():
    status_name = request.form.get("status_name")
    res=status_Model.add_status(status_name)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))


@status_blueprint.route("/updatestatus",methods=['post'])
@cross_origin()
def update_status_disabled():
    global update_status
    status_id=request.form.get("status_id")
    status_isdisable = request.form.get("status_isdisable")
    if status_isdisable=='1':
        update_status='0'
    if status_isdisable=='0':
        update_status='1'
    res=status_Model.updatestatus(status_id,update_status)
    if res==1:
        return jsonify(to_dict_code('20004',data=None))
    return jsonify(to_dict_code('20005',data=None))


@status_blueprint.route("/test4")
def test4():
    list=status_Model.get_name_list()
    return 'ok'


