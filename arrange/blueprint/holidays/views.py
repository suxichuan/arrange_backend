from . import special_holidays,special_holidays_api
from arrange.models.minorityFamilyHolidaysModel import minorityFamilyHolidays
from flask_cors import cross_origin
from flask import jsonify,request
from arrange.utils.code import to_dict_code
from flask_restful import Resource
minorityFamilyHolidaysModel=minorityFamilyHolidays()

class specialHolidays_(Resource):
    def get(self):
        pass
    def post(self):
        holiday_name=request.form.get("holiday_name")
        start=request.form.get("start")
        end=request.form.get("end")
        comment=request.form.get("comment")
        res=minorityFamilyHolidaysModel.add_minority_family_holidays(holidays_name=holiday_name,start=start,end=end,comments=comment)
        if res == 1:
            return jsonify(to_dict_code('20004',data=None))
        return jsonify(to_dict_code('20005',data=None))
special_holidays_api.add_resource(specialHolidays_,'/add')



@special_holidays.route("/list", methods=['get'])
@cross_origin()
def get_special_holidays_list():
    current_page = int(request.args.get("current_page"))
    page_size = int(request.args.get("page_size"))
    keyword = request.args.get("keyword")
    if keyword == 'null':
        keyword = None
    if current_page < 1:
        current_page = 1
    offset = (current_page - 1) * page_size
    res = minorityFamilyHolidaysModel.get_spacial_holiday_list(keyword,offset,page_size)
    holiday_list = res[0]
    holiday_ls = []
    for holiday in holiday_list:
        r = holiday.serialization()
        holiday_ls.append(r)
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
                'list': holiday_ls
            }
    }
    return jsonify(to_dict_code('20000', data=data))


@special_holidays.route("/update",methods=['post'])
@cross_origin()
def update_holiday():
    holiday_id = request.form.get("id")
    holiday_name = request.form.get("holiday_name")
    start = request.form.get("start")
    end = request.form.get("end")
    comment = request.form.get("comment")
    res=minorityFamilyHolidaysModel.update_holiday(holiday_id,holiday_name,start,end,comment)
    # res=placeModel.update_place(place_code,place_name)
    if res==1:
        return jsonify(to_dict_code('20004',data=None))
    return jsonify(to_dict_code('20005',data=None))



@special_holidays.route("/delete",methods=['get'])
@cross_origin()
def delete_holiday_by_id():
    holiday_id=request.args.get("holiday_id")
    res=minorityFamilyHolidaysModel.delete_holiday_by_id(holiday_id)
    if res == 1:
        return jsonify(to_dict_code('20004', data=None))
    return jsonify(to_dict_code('20005', data=None))