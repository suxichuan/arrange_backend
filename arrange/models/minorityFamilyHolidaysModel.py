
from . import minority_family_holidays
from arrange.utils import db
from sqlalchemy import and_
from arrange.utils.date_tool import datetool
# id = db.Column(db.Integer, primary_key=True)
#     holidays_name=db.Column(db.String(64),unique=True,nullable=False)
#     start_time = db.Column(db.Date, default=date.today())
#     end_time = db.Column(db.Date, default=date.today())
#     comments=db.Column(db.String(255))

class minorityFamilyHolidays():

    minority_family_holidays_model=minority_family_holidays()
    dt = datetool()
    
    def add_minority_family_holidays(self,holidays_name,start,end,comments):
        minority = minority_family_holidays(holidays_name=holidays_name,
                          start_time=start, end_time=end,comments=comments)
        try:
            db.session.add(minority)
            db.session.commit()
            res=1
        except Exception:
            db.session.rollback()
            res=0
        return res

    def get_spacial_holiday_list(self,keyword,offset,limit):
        if keyword is not None:
            list=self.minority_family_holidays_model.query.filter(minority_family_holidays.holidays_name.like('%{}%'.format(keyword))).offset(offset).limit(limit).all()
            cnt=self.minority_family_holidays_model.query.filter(minority_family_holidays.holidays_name.like('%{}%'.format(keyword))).count()
        else:
            list = self.minority_family_holidays_model.query.offset(
                offset).limit(limit).all()
            cnt = self.minority_family_holidays_model.query.count()
        return list,cnt


    def get_holiday_by_id(self,holiday_id):
        holiday_inst=self.minority_family_holidays_model.query.filter_by(id=holiday_id).first()
        return holiday_inst


    def update_holiday(self,holiday_id,holiday_name,start,end,comment):
        holiday_obj = self.minority_family_holidays_model.query.filter_by(id=holiday_id).first()
        if holiday_obj is not None:
            try:
                holiday_obj.holidays_name=holiday_name
                holiday_obj.start_time=start
                holiday_obj.end_time=end
                holiday_obj.comments=comment
                db.session.commit()
                res=1
            except Exception:
                res=0
        else:
            res=0
        return res

    def delete_holiday_by_id(self,holiday_id):
        holiday_obj=self.minority_family_holidays_model.query.filter_by(id=holiday_id).first()
        if holiday_obj is not None:
            try:
                db.session.delete(holiday_obj)
                db.session.commit()
                res=1
            except Exception:
                res = 0
            return  res
        else:
            return 0

    def holiday_list(self):
        times=self.dt.get_first_and_end_of_month()
        first_day=times[0]
        last_day=times[1]
        holiday_list=self.minority_family_holidays_model.query.\
            filter(and_(minority_family_holidays.start_time>=first_day,minority_family_holidays.end_time<=last_day)).\
            with_entities(minority_family_holidays.start_time,minority_family_holidays.end_time,minority_family_holidays.holidays_name).all()
        return holiday_list
