from . import dutyPlan
from arrange.utils import db
from sqlalchemy import and_
from datetime import date
from arrange.utils.date_tool import datetool
from sqlalchemy import func, desc


class duty_plan():
    duty_plan_model = dutyPlan()
    dt = datetool()

    def add_duty_plan_bitch(self, list):
        if len(list) > 0:
            try:
                db.session.add_all(list)
                db.session.commit()
                res = 1
            except Exception:
                db.session.rollback()
                res = 0
            return res

    def get_month_duty_plan_list(self):
        months_week = self.dt.get_months_of_year()
        first_day = months_week[0][0]
        last_day = months_week[-1][-1]
        plans = self.duty_plan_model.query.filter(
            and_(dutyPlan.duty_plan_date.between(first_day, last_day), dutyPlan.status == 1,
                 dutyPlan.duty_type == 'month')).order_by(dutyPlan.duty_plan_date).all()
        return plans

    def check_the_month_plan(self):
        months_week = self.dt.get_months_of_year()
        first_day = months_week[0][0]
        last_day = months_week[-1][-1]
        cnt = self.duty_plan_model.query.filter(
            and_(dutyPlan.duty_plan_date.between(first_day, last_day), dutyPlan.status == 1,
                 dutyPlan.duty_type == 'month')).count()
        return cnt

    def update_status_the_month_plan(self):
        try:
            self.duty_plan_model.query.filter(
                and_(dutyPlan.status == 1, dutyPlan.duty_type == 'month')).update({'status': 0})
            db.session.commit()
            return 1
        except Exception:
            db.session.rollback()
            return 0

    def get_current_date_duty_plan(self):
        now = date.today()
        list = self.duty_plan_model.query.filter(and_(dutyPlan.duty_plan_date == now, dutyPlan.status == 1)).all()
        return list

    def get_week_duty_plan_list(self):
        weeks = self.dt.get_weeks_of_month()
        first_day = weeks[0]
        last_day = weeks[-1]
        plans = self.duty_plan_model.query.filter(
            and_(dutyPlan.duty_plan_date.between(first_day, last_day), dutyPlan.status == 1,
                 dutyPlan.duty_type == 'week')).all()
        return plans

    def check_the_week_plan(self):
        weeks = self.dt.get_weeks_of_month()
        first_day = weeks[0]
        last_day = weeks[-1]
        cnt = self.duty_plan_model.query.filter(
            and_(dutyPlan.duty_plan_date.between(first_day, last_day), dutyPlan.status == 1,
                 dutyPlan.duty_type == 'week')).count()
        return cnt

    def update_status_the_week_plan(self):
        try:
            self.duty_plan_model.query.filter(
                and_(dutyPlan.status == 1, dutyPlan.duty_type == 'week')).update({'status': 0})
            db.session.commit()
            return 1
        except Exception:
            db.session.rollback()
            return 0

    def get_current_month_duty_plan(self):
        now = date.today()
        list = self.duty_plan_model.query.filter(
            and_(dutyPlan.duty_plan_date == now, dutyPlan.status == 1, dutyPlan.duty_type == 'month')).all()
        return list

    def get_current_week_duty_plan(self):
        now = date.today()
        list = self.duty_plan_model.query.filter(
            and_(dutyPlan.duty_plan_date == now, dutyPlan.status == 1, dutyPlan.duty_type == 'week')).all()
        return list

    def get_current_self_established_duty_plan(self):
        now = date.today()
        list = self.duty_plan_model.query.filter(
            and_(dutyPlan.duty_plan_date == now, dutyPlan.status == 1, dutyPlan.duty_type == 'establish')).all()
        return list

    def analyse(self):
        res = db.session.query(dutyPlan.staff_code, func.count(1).label('cnt')).group_by(dutyPlan.staff_code).order_by(
            desc('cnt')).offset(0).limit(30).all()
        return res

    def update_status_by_staff_code(self, staff_code):
        global count
        try:
            count=self.duty_plan_model.query.filter(and_(dutyPlan.staff_code == staff_code, dutyPlan.status == 1)).update(
                {'status': 0})
            db.session.commit()
            ret = count
        except Exception:
            ret = count
        return ret

    def get_staff_by_staff_code(self,staff_code):
        sta_list=self.duty_plan_model.query.with_entities(
            dutyPlan.duty_plan_date,
            dutyPlan.duty_place_code,
            dutyPlan.duty_type,
            dutyPlan.is_week,
            dutyPlan.comment,dutyPlan.is_working)\
            .filter(and_(dutyPlan.staff_code == staff_code, dutyPlan.status == 1)).all()
        # [(datetime.date(2024, 3, 26), '10004', 'month', '星期二', None, 1)]
        res_list=[]
        if len(sta_list)>0:
            for item in sta_list:
                res_list.append({'duty_plan_date':item[0],'duty_place_code':item[1],'duty_type':item[2],'is_week':item[3],'comment':item[4],'is_working':item[5]})
        return res_list
