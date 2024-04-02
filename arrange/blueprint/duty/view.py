from . import duty_api,duty_blueprint
from arrange.models.dutyPlanModel import duty_plan
from arrange.models.staffModel import staff_model
from arrange.models.placeOfDutyModel import place_duty_model
from arrange.models.minorityFamilyHolidaysModel import minorityFamilyHolidays
from arrange.utils.arrange import to_arrange
from arrange.models import dutyPlan
from arrange.utils.code import to_dict_code
from flask import jsonify
from arrange.utils.json_tool import to_json_list,to_dict_json_list,process_current_duty_list

from flask_cors import  cross_origin

staff_Model = staff_model()
place_Model = place_duty_model()
duty_plan_Model=duty_plan()
minorityFamilyHolidaysModel=minorityFamilyHolidays()


@duty_blueprint.route("/arrange_month",methods=['get'])
@cross_origin()
def add_duty_plan_month():
    cnt=duty_plan_Model.check_the_month_plan()
    if cnt>0:
        duty_plan_Model.update_status_the_month_plan()
    staff_ids=staff_Model.get_staff_by_status_and_role()
    place_config=place_Model.get_place_list_by_status()
    arrange=to_arrange()
    holiday_list=minorityFamilyHolidaysModel.holiday_list()
    plan_list=arrange.arrange_staff_to_duty_per_month(staff_list=staff_ids,place_config=place_config,special_holiday_list=holiday_list)
    duty_plan_list=[]
    for duty in plan_list:
        duty_obj=dutyPlan(
            duty_plan_date=duty.get('dutydate'),
            duty_type=duty.get('type'),
            is_working=duty.get('is_work'),
            comment=duty.get('comment'),
            staff_code=duty.get('dutystaff'),
            duty_place_code=duty.get('dutyplace'),
            is_week=duty.get('is_week')
        )
        duty_plan_list.append(duty_obj)
    res=duty_plan_Model.add_duty_plan_bitch(duty_plan_list)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))

@duty_blueprint.route("/arrange_month_clear",methods=['get'])
@cross_origin()
def duty_plan_month_clear():
    res=duty_plan_Model.update_status_the_month_plan()
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))


@duty_blueprint.route("/get_month_duty_plan",methods=['get'])
@cross_origin()
def add_duty_plan_check():
    month_plans=duty_plan_Model.get_month_duty_plan_list()
    month_plans_list=[]
    if month_plans is not None:
        for plan in month_plans:
            ret = plan.serialization()
            month_plans_list.append(ret)
    ls=to_dict_json_list(to_json_list(month_plans_list))
    if month_plans_list is not None:
        return jsonify(to_dict_code('20000', data=ls))
    return jsonify(to_dict_code('20008', data=ls))

@duty_blueprint.route("/arrange_week",methods=['get'])
@cross_origin()
def add_duty_plan_week():
    cnt = duty_plan_Model.check_the_week_plan()
    if cnt > 0:
        duty_plan_Model.update_status_the_week_plan()
    arrange = to_arrange()
    staff_ids = staff_Model.get_staff_by_status_and_role()
    place_config=place_Model.get_place_list_by_status()
    holiday_list = minorityFamilyHolidaysModel.holiday_list()
    duty_week_plan_list=arrange.arrange_staff_to_duty_per_week(staff_code_list=staff_ids,place_config=place_config,special_holiday_list=holiday_list)
    duty_plan_list = []
    for duty in duty_week_plan_list:
        duty_obj = dutyPlan(
            duty_plan_date=duty.get('dutydate'),
            duty_type=duty.get('type'),
            is_working=duty.get('is_work'),
            comment=duty.get('comment'),
            staff_code=duty.get('dutystaff'),
            duty_place_code=duty.get('dutyplace'),
            is_week = duty.get('is_week')
        )
        duty_plan_list.append(duty_obj)
    res = duty_plan_Model.add_duty_plan_bitch(duty_plan_list)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))

@duty_blueprint.route("/get_week_duty_plan",methods=['get'])
@cross_origin()
def get_duty_week_plan():
    week_plans=duty_plan_Model.get_week_duty_plan_list()
    week_plans_list=[]
    if week_plans is not None:
        for plan in week_plans:
            ret = plan.serialization()
            week_plans_list.append(ret)
    ls=to_dict_json_list(to_json_list(week_plans_list))
    if ls is not None:
        return jsonify(to_dict_code('20000', data=ls))
    return jsonify(to_dict_code('20005', data=ls))


@duty_blueprint.route("/arrange_week_clear",methods=['get'])
@cross_origin()
def duty_plan_week_clear():
    res=duty_plan_Model.update_status_the_week_plan()
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))


@duty_blueprint.route("/current_duty_month_list",methods=['get'])
@cross_origin()
def get_current_duty_month_list_method():
    res=duty_plan_Model.get_current_month_duty_plan()
    ls=[]
    for i in res:
        ret=i.serialization()
        ls.append(ret)
    if ls is not None:
        return jsonify(to_dict_code('20000', data=process_current_duty_list(ls)))
    return jsonify(to_dict_code('20005', data=ls))


@duty_blueprint.route("/current_duty_week_list",methods=['get'])
@cross_origin()
def get_current_duty_week_list_method():
    res=duty_plan_Model.get_current_week_duty_plan()
    ls=[]
    for i in res:
        ret=i.serialization()
        ls.append(ret)
    if ls is not None:
        return jsonify(to_dict_code('20000', data=process_current_duty_list(ls)))
    return jsonify(to_dict_code('20005', data=ls))


@duty_blueprint.route("/analyse",methods=['get'])
@cross_origin()
def analyse_method():
    global names_and_code, res
    ret=duty_plan_Model.analyse()
    if len(ret)>0:
        staff_codes=[]
        ls=[]
        for res in ret:
            if res[0] is None:
                continue
            staff_codes.append(res[0])
            ls.append(res)
        names_and_code=staff_Model.get_staff_name_by_ids(staff_codes)
    name_dict={item[1]:item[0] for item in names_and_code}
    name_list=[]
    count_list=[]
    for i in ls:
        staff_code=i[0]
        cnt=i[1]
        name=name_dict.get(staff_code)
        name_list.append(name)
        count_list.append(cnt)
    res_list={'namelist':name_list,'count':count_list}
    if res_list is not None:
        return jsonify(to_dict_code('20000', data=res_list))
    return jsonify(to_dict_code('20005', data=res_list))