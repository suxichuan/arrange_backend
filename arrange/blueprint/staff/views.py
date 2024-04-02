from . import staff_blueprint, staff_api
from arrange.models.staffModel import staff_model, staff as sta
from arrange.models.statusModel import status_model
from arrange.models.roleModel import role_model
from arrange.models.dutyPlanModel import duty_plan
from arrange.utils.arrange import to_arrange
from flask import request, jsonify, make_response
from arrange.utils.code import to_dict_code
from flask_cors import cross_origin
from flask_restful import Resource
import pandas as pd
import io
import pickle
from arrange.utils.json_tool import to_dict,serializable_staff_status_analyse

from ...models import dutyPlan

staff_model = staff_model()
staff_status_model = status_model()
staff_role_model = role_model()
duty_model = duty_plan()
arrange_obj = to_arrange()


class staff(Resource):
    def get(self):
        pass

    def post(self):
        staff_code = request.form.get("staff_code")
        staff_name = request.form.get("staff_name")
        staff_tel = request.form.get("staff_tel")
        staff_address = request.form.get("staff_address")
        staff_email = request.form.get("staff_email")
        staff_status_id = request.form.get("staff_status")
        staff_role_id = request.form.get("staff_role")
        staff_obj = sta()
        staff_obj.staff_code = staff_code
        staff_obj.staff_name = staff_name
        staff_obj.staff_tel = staff_tel
        staff_obj.staff_address = staff_address
        staff_obj.staff_email = staff_email
        staff_obj.staff_status_id = staff_status_id
        staff_obj.staff_role_id = staff_role_id
        res = staff_model.add_staff(staff_obj)
        if res == 1:
            return jsonify(to_dict_code('20001', data=None))
        return jsonify(to_dict_code('20002', data=None))


staff_api.add_resource(staff, "/add", methods=['post'])


@staff_blueprint.route("/addbatch", methods=['post'])
@cross_origin()
def staff_add_batch():
    file = request.files['file']
    df = pd.read_excel(file.stream, index_col=0)
    staff_list = []
    # ['人员编码', '人员名称', '联系方式', '联系地址', '电子邮件', '人员状态']rowobj['人员编码'], rowobj['人员名称'], rowobj['联系方式'], rowobj['联系地址'], rowobj['电子邮件'], rowobj['人员状态']
    # ['出差','驻村','请假','局领导','休假','在岗']
    for i in df.index:
        rowobj = df.loc[i]
        status_id = staff_status_model.get_status_id_by_name(rowobj['人员状态'])
        role_id = staff_role_model.get_role_id_by_name(rowobj['人员角色'])

        staffobj = sta(staff_name=rowobj['人员名称'],
                       staff_code=rowobj['人员编码'],
                       staff_tel=rowobj['联系方式'],
                       staff_address=rowobj['联系地址'],
                       staff_email=rowobj['电子邮件'],
                       staff_status_id=status_id,
                       staff_role_id=role_id
                       )
        staff_list.append(staffobj)
    res = staff_model.add_staff_bitch(staff_list)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))


@staff_blueprint.route("/delete", methods=['get'])
@cross_origin()
def delete_staff():
    staff_code = request.args.get("staff_code")
    res = staff_model.delete_staff(staff_code)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))


@staff_blueprint.route("/deletebitch", methods=['get'])
@cross_origin()
def delete_staff_bitch():
    ids = request.args.get("ids")
    ls = ids.split(',')
    res = staff_model.delete_all(ls)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))


@staff_blueprint.route("/list", methods=['get'])
@cross_origin()
def get_staff_list():
    current_page = int(request.args.get("current_page"))
    page_size = int(request.args.get("page_size"))
    staff_name = request.args.get("key_employee_name")
    staff_code = request.args.get("key_employee_code")
    if staff_name == 'null':
        staff_name = None
    if staff_code == 'null':
        staff_code = None
    if current_page < 1:
        current_page = 1
    offset = (current_page - 1) * page_size
    res = staff_model.get_staff_list(offset, page_size, staff_name, staff_code)
    staff_list = res[0]
    ser_ls = []
    for stf in staff_list:
        r = stf.serialization()
        ser_ls.append(r)
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
                'list': ser_ls
            }
    }
    return jsonify(to_dict_code('20000', data=data))


@staff_blueprint.route("/export_template", methods=['get'])
@cross_origin()
def staff_export_template():
    data = []
    data.append(('10001', '苏赫1', '18148053811', '嘎吉康萨', '714783552@qq.com', ''))
    data.append(('10002', 'hudi', '18148053812', '德吉北路', '714783552@qq.com', ''))
    data.append(('10003', 'kudi', '18148053813', '北京中路', '714783552@qq.com', ''))
    data.append(('10004', '西溪', '18148053814', '巴尔库路', '714783552@qq.com', ''))
    column = ['人员编码', '人员名称', '联系方式', '联系地址', '电子邮件', '人员状态']
    ds = pd.DataFrame(data=data, columns=column)
    bio = io.BytesIO()
    writer = pd.ExcelWriter(bio, engine='xlsxwriter')
    ds.to_excel(writer, sheet_name='人员信息导入模板')
    workbook = writer.book
    worksheet = writer.sheets['人员信息导入模板']

    status_list = staff_status_model.get_name_list()
    if status_list is None:
        status_list = []
    worksheet.data_validation(first_row=1, first_col=6, last_row=65535, last_col=6, options={'validate': 'list',
                                                                                             'source': status_list})
    worksheet.write('H1', '人员角色')
    role_list = staff_role_model.get_name_list()
    if role_list is None:
        role_list = []
    worksheet.data_validation(first_row=1, first_col=7, last_row=65535, last_col=7, options={'validate': 'list',
                                                                                             'source': role_list})
    workbook.close()
    bio.seek(0)  # 文件指针
    rv = make_response(bio.getvalue())
    bio.close()
    rv.headers['Content-Type'] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    rv.headers["Cache-Control"] = "no-cache"
    rv.headers['Content-Disposition'] = 'attachment; filename={}.xlsx'.format('staff_template')
    return rv


@staff_blueprint.route("/update_info", methods=['post'])
@cross_origin()
def update_staff_info_by_id():
    staff_code = request.form.get("staff_code")
    staff_name = request.form.get("staff_name")
    staff_tel = request.form.get("staff_tel")
    staff_address = request.form.get("staff_address")
    staff_email = request.form.get("staff_email")
    staff_status_id = int(request.form.get("staff_status_id"))
    staff_role_id = int(request.form.get("staff_role_id"))
    original_data = staff_model.get_status_and_role_by_staff_code(staff_code)
    status_id = original_data[0]
    role_id = original_data[1]
    staff_obj = sta()
    staff_obj.staff_code = staff_code
    staff_obj.staff_name = staff_name
    staff_obj.staff_tel = staff_tel
    staff_obj.staff_address = staff_address
    staff_obj.staff_email = staff_email
    staff_obj.staff_status_id = staff_status_id
    staff_obj.staff_role_id = staff_role_id
    res = staff_model.update_staff_by_code(staff_obj)
    role_disabled_list = staff_role_model.get_role_list_by_disabled()
    status_disabled_list = staff_status_model.get_status_disabled_list()
    if (status_id != staff_status_id or role_id != staff_role_id) and res == 1:
        if staff_status_id in status_disabled_list or staff_role_id in role_disabled_list:
            from arrange.utils.redis_queue import RedisQueue
            weekredisQueue = RedisQueue(name='week_plan')
            monthredisQueue = RedisQueue(name='month_plan')
            weekredisQueue.rem_queue_element(pickle.dumps(staff_code))
            monthredisQueue.rem_queue_element(pickle.dumps(staff_code))
            equailize_duty_ls = duty_model.get_staff_by_staff_code(staff_code)
            cnt = duty_model.update_status_by_staff_code(staff_code)
            if len(equailize_duty_ls) == cnt and cnt > 0:
                # 进行排班补偿
                equalize_duty_list = arrange_obj.equailize_duty_plan(equailize_duty_ls)
                duty_plan_list = []
                for duty in equalize_duty_list:
                    duty_obj = dutyPlan(
                        duty_plan_date=duty.get('dutydate'),
                        duty_type=duty.get('type'),
                        is_working=duty.get('is_work'),
                        comment=duty.get('comment'),
                        staff_code=duty.get('dutystaff'),
                        duty_place_code=duty.get('dutyplace'),
                        is_week=duty.get('is_week')
                    )
                    duty_plan_list.append(duty_obj)
                duty_model.add_duty_plan_bitch(duty_plan_list)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))


@staff_blueprint.route("/analyse", methods=['get'])
@cross_origin()
def analyse_staff_status():
    data=staff_model.analyse()
    status_list=staff_status_model.get_list()
    res_data=serializable_staff_status_analyse(data,to_dict(status_list))
    if res_data is not None:
        return jsonify(to_dict_code('20004', data=res_data))
    else:
        return jsonify(to_dict_code('20005', data={}))


# @staff_blueprint.route("/percentage_analyse", methods=['get'])
# @cross_origin()
# def staff_status_percentage_analyse():
#     data=staff_model.analyse()
#     status_list=staff_status_model.get_list()
#     if len(data)>0:
#         for item in data:
#
#     res_data=[]
#     if res_data is not None:
#         return jsonify(to_dict_code('20004', data=res_data))
#     else:
#         return jsonify(to_dict_code('20005', data={}))
