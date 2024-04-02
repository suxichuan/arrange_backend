from . import place_blueprint,place_api
from arrange.models.placeOfDutyModel import place_duty_model
from flask_cors import cross_origin
from flask import jsonify,request
from arrange.utils.code import to_dict_code
from flask_restful import Resource

placeModel=place_duty_model()

@place_blueprint.route("/list",methods=['get'])
@cross_origin()
def get_place_list():
    current_page = int(request.args.get("current_page"))
    page_size = int(request.args.get("page_size"))
    place_code = request.args.get("key_place_code")
    place_name = request.args.get("key_place_name")
    if place_name == 'null':
        place_name = None
    if place_code ==  'null':
        place_code=None
    if current_page < 1:
        current_page = 1
    offset=(current_page-1)*page_size
    place_list_count=placeModel.get_place_list(offset=offset,limit=page_size,place_name=place_name,place_code=place_code)
    place_list=place_list_count[0]
    total = int(place_list_count[1])
    if place_list is not None and len(place_list)>0:
        ls = []
        for place in place_list:
            r=place.serialization()
            ls.append(r)
        data={
            'list':ls,
            'total': total,
            'current_page':current_page
        }
        return jsonify(to_dict_code('20000',data=data))
    else:
        return jsonify(to_dict_code('20008',data=None))


@place_blueprint.route("/updatestatus",methods=['post'])
@cross_origin()
def update_place_status():
    global update_status
    place_code=request.form.get("place_code")
    place_status = request.form.get("place_status")
    if place_status=='1':
        update_status='0'
    if place_status=='0':
        update_status='1'
    res=placeModel.updatestatus(place_code,update_status)
    if res==1:
        return jsonify(to_dict_code('20004',data=None))
    return jsonify(to_dict_code('20005',data=None))

@place_blueprint.route("/delete",methods=['get'])
@cross_origin()
def delete_place():
    place_code=request.args.get("place_code")
    res=placeModel.delete_place(place_code)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))

@place_blueprint.route("/update",methods=['post'])
@cross_origin()
def update_place():
    place_code = request.form.get("place_code")
    place_name = request.form.get("place_name")
    place_num = request.form.get("place_num")
    res=placeModel.update_place(place_code,place_name,place_num)
    if res==1:
        return jsonify(to_dict_code('20004',data=None))
    return jsonify(to_dict_code('20005',data=None))


class place(Resource):
    def get(self):
        pass
    def post(self):
        place_name=request.form.get("place_name")
        place_code=request.form.get("place_code")
        place_num=request.form.get("place_num")
        res=placeModel.add(place_code,place_name,place_num)
        if res == 1:
            return jsonify(to_dict_code('20004',data=None))
        return jsonify(to_dict_code('20005',data=None))
place_api.add_resource(place,'/add')

@place_blueprint.route("/checkcode",methods=['get'])
@cross_origin()
def check_code():
    place_code = request.args.get("place_code")
    print(place_code)
    res=placeModel.check_code(place_code)
    if res==1:
        return jsonify(to_dict_code('20006',data=None))
    return jsonify(to_dict_code('20007',data=None))


# @place_blueprint.route("/export")
# def export_list():
#     place_list=placeModel.get_place_list(0,5)
#     data=[]
#     for place in place_list:
#         r=place.serialization()
#         data.append(r)
#     print(data)
#     response = make_response(write_to_excel(data))
#     response.headers["Content-Disposition"] = "attachment; filename=data.xls"
#     return response


# def write_to_excel(data):
#     # Create workbook and worksheet objects
#     book = xlwt.Workbook(encoding="utf-8")
#     sheet1 = book.add_sheet("值班人员名单")
#     # Write data to worksheet
#     for row_index, row_data in enumerate(data):
#         for column_index, col_data in enumerate(row_data):
#             sheet1.write(row_index, column_index, col_data)
#     # Save workbook to string buffer
#     output = io.BytesIO()
#     book.save(output)
#     output.seek(0)
#     return output.getvalue()

# """
#    staff_id=db.Column(db.Integer,primary_key=True)
#     staff_code=db.Column(db.String(64),unique=True,nullable=False)
#     staff_name=db.Column(db.String(32))
#     staff_tel=db.Column(db.String(11))
#     staff_address=db.Column(db.String(256))
#     staff_email=db.Column(db.String(256))
#     staff_status=db.Column(db.String(1))
# """

# def write_to_excel(data):
#     headers = (u"人员id",u"人员编码", u"姓名", u"电话",u"联系地址",u"电子邮件","人员状态")
#     data1 = tablib.Dataset(data, headers=headers)
#     book = tablib.Databook(data1)
#     output = io.BytesIO()
#     book.save(output)
#     output.seek(0)
#     return output.getvalue()
