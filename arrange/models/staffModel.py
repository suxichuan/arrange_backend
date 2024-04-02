from arrange.utils import db
from . import staff
from sqlalchemy import and_,func,desc
from .roleModel import role_model
from .statusModel import status_model



class staff_model():
    staff_Model = staff()
    role_Model=role_model()
    status_Model=status_model()

    def add_staff(self, staff_obj):
            try:
                db.session.add(staff_obj)
                db.session.commit()
                return 1
            except Exception:
                db.session.rollback()
                return 0

    def delete_staff(self, staff_code):
        staff_obj = self.staff_Model.query.filter_by(staff_code=staff_code).first()
        res=0
        if staff_obj is not None:
            try:
                db.session.delete(staff_obj)
                db.session.commit()
                res = 1
            except Exception:
                db.session.rollback()
                res = 0
        return res

    def add_staff_bitch(self, list):
        if len(list)>0:
            try:
                db.session.add_all(list)
                db.session.commit()
                res = 1
            except Exception:
                db.session.rollback()
                res = 0
            return res


    def get_staff_list(self,offset, limit, staff_name, staff_code):
        try:
            if staff_name is not None and staff_code is not None:
                staff_list = self.staff_Model.query.filter(
                    and_(staff.staff_name.like('%{}%'.format(staff_name)),
                         staff.staff_code.like('%{}%'.format(staff_code)))).offset(offset).limit(limit).all()
                staff_count = self.staff_Model.query.filter(
                    and_(staff.staff_name.like('%{}%'.format(staff_name)),
                         staff.staff_code.like('%{}%'.format(staff_code)))).count()
                return (staff_list, staff_count)
            if staff_code is not None:
                staff_list = self.staff_Model.query.filter(
                    staff.staff_code.like('%{}%'.format(staff_code))).offset(offset).limit(limit).all()
                staff_count = self.staff_Model.query.filter(
                    staff.staff_code.like('%{}%'.format(staff_code))).count()
                return (staff_list, staff_count)
            if staff_name is not None:
                staff_list = self.staff_Model.query.filter(
                    staff.staff_name.like('%{}%'.format(staff_name))).offset(offset).limit(limit).all()
                staff_count = self.staff_Model.query.filter(
                    staff.staff_name.like('%{}%'.format(staff_name))).count()
                return (staff_list, staff_count)
            if staff_name is None and staff_code is None:
                staff_list = self.staff_Model.query.offset(offset).limit(limit).all()
                staff_count = self.staff_Model.query.count()
                return (staff_list, staff_count)
        except Exception:
            return (None, 0)
        return (None, 0)


    def delete_all(self,list):
        staff_list = self.staff_Model.query.filter(staff.staff_code.in_(list)).all()
        if len(staff_list)>0:
            try:
                for i in staff_list:
                    db.session.delete(i)
                    db.session.commit()
                return 1
            except Exception:
                db.session.rollback()
                return 0
        else:
            return 0

    def get_staff_by_status_and_role(self):
        role_isdisable_list=self.role_Model.get_role_isdisable_list()
        status_isdisable_list=self.status_Model.get_status_isdisable_list()
        if role_isdisable_list is None:
            role_isdisable_list=['']
        if status_isdisable_list is None:
            status_isdisable_list=['']
        staff_list=self.staff_Model.query.filter(and_(staff.staff_role_id.in_(role_isdisable_list),staff.staff_status_id.in_(status_isdisable_list))).with_entities(staff.staff_code).all()
        if len(staff_list)>0:
            ids=[i[0] for i in staff_list]
            return ids
        else:
            return None

    def get_staff_name_by_ids(self,ids):
        staff_names=self.staff_Model.query.with_entities(staff.staff_name,staff.staff_code).filter(staff.staff_code.in_(ids)).all()
        return staff_names


    def update_staff_by_code(self, staff_):
        global res
        staff_obj = self.staff_Model.query.filter_by(staff_code=staff_.staff_code).first()
        if staff_obj is not None:
            try:
                staff_obj.staff_name = staff_.staff_name
                staff_obj.staff_tel = staff_.staff_tel
                staff_obj.staff_address = staff_.staff_address
                staff_obj.staff_email = staff_.staff_email
                staff_obj.staff_status_id = staff_.staff_status_id
                staff_obj.staff_role_id = staff_.staff_role_id
                db.session.commit()
                res = 1
            except Exception:
                res = 0
        return res


    def get_status_and_role_by_staff_code(self,staff_code):
        status_and_role=self.staff_Model.query.with_entities(staff.staff_status_id,staff.staff_role_id).filter_by(staff_code=staff_code).first()
        return status_and_role



    def analyse(self):
        res = db.session.query(staff.staff_status_id, func.count(1).label('cnt')).group_by(staff.staff_status_id).order_by(
            desc('cnt')).all()
        return res



