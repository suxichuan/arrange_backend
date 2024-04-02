from arrange.utils import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime,date


class baseModel:
    create_time=db.Column(db.DateTime,default=datetime.now)
    update_time=db.Column(db.DateTime,default=datetime.now,onupdate=datetime.now)

class user(db.Model,baseModel):
    __tablename__= 't_user'
    userid=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(32),unique=True,nullable=False)
    pwd=db.Column(db.String(256))
    nickname=db.Column(db.String(64))
    phone=db.Column(db.String(11))
    email=db.Column(db.String(254))

    @property
    def password(self):
        return self.pwd

    @password.setter
    def password(self,t_pwd):
        self.pwd=generate_password_hash(t_pwd)

    def check_password(self,t_pwd):
        return check_password_hash(self.pwd,t_pwd)
from .user_model import usermodel

class admin(db.Model,baseModel):
    __tablename__ = 't_admin'
    adminid = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(64), unique=True)
    passwd = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(32))
    nickname = db.Column(db.String(64))
    telephone = db.Column(db.String(11))
    email = db.Column(db.String(256))

    @property
    def password(self):
        return self.passwd

    @password.setter
    def password(self, t_passwd):
        self.passwd = generate_password_hash(t_passwd)

    def check_passwd(self, t_passwd):
        return check_password_hash(self.passwd, t_passwd)



class dutyPlace(db.Model,baseModel):
    __tablename__ = 't_place'
    duty_place_id=db.Column(db.Integer,primary_key=True)
    duty_place_code=db.Column(db.String(32),unique=True)
    duty_place_name=db.Column(db.String(256))
    duty_place_num=db.Column(db.Integer)
    #在数据库中Boolean是tinyint true是0，false是1
    is_deleted = db.Column(db.Boolean,default=False,nullable=False)
    duty_place_status=db.Column(db.String(1),default='1')

    def serialization(self):
        return {
            'place_id': self.duty_place_id,
            'place_code': self.duty_place_code,
            'place_name': self.duty_place_name,
            'duty_place_num': self.duty_place_num,
            'place_status':self.duty_place_status,
            'update_time':self.update_time,
            'create_time':self.create_time,
        }

class sys_status(db.Model,baseModel):
    __tablename__='t_sys_status'
    status_id = db.Column(db.Integer,primary_key=True)
    status_name = db.Column(db.String(32))
    status_isdisable =  db.Column(db.String(1),default='1')
    staff = db.relationship('staff',back_populates='sys_status')

    def serialization(self):
        return {
            'status_id': self.status_id,
            'status_name': self.status_name,
            'status_isdisable': self.status_isdisable,
            'update_time':self.update_time,
            'create_time':self.create_time,
        }

class sys_role(db.Model,baseModel):
    __tablename__='t_sys_role'
    role_id = db.Column(db.Integer,primary_key=True)
    role_name = db.Column(db.String(32),unique=True,nullable=False)
    role_isdisable = db.Column(db.String(1), default='1')
    staff = db.relationship('staff',back_populates='sys_role')

    def serialization(self):
        return {
            'role_id': self.role_id,
            'role_name': self.role_name,
            'role_isdisable': self.role_isdisable,
            'update_time':self.update_time,
            'create_time':self.create_time,
        }

class staff(db.Model,baseModel):
    __tablename__='t_staff'
    staff_id=db.Column(db.Integer,primary_key=True)
    staff_code=db.Column(db.String(64),unique=True,nullable=False)
    staff_name=db.Column(db.String(32))
    staff_tel=db.Column(db.String(11))
    staff_address=db.Column(db.String(256))
    staff_email=db.Column(db.String(256))
    staff_status_id = db.Column(db.Integer,db.ForeignKey('t_sys_status.status_id')) #此处应该使用表名
    staff_role_id = db.Column(db.Integer,db.ForeignKey('t_sys_role.role_id'))
    sys_status = db.relationship('sys_status', primaryjoin=(sys_status.status_id == staff_status_id))
    # sys_status = db.relationship('sys_status')
    sys_role = db.relationship('sys_role',primaryjoin=(sys_role.role_id == staff_role_id))
    # sys_role = db.relationship('sys_role')

    def serialization(self):
        return {
            'staff_id': self.staff_id,
            'staff_code': self.staff_code,
            'staff_name': self.staff_name,
            'staff_tel':self.staff_tel,
            'staff_address':self.staff_address,
            'staff_email':self.staff_email,
            'staff_role_id':self.staff_role_id,
            'staff_status_id':self.staff_status_id,
            'staff_status':self.sys_status.status_name,
            'staff_role':self.sys_role.role_name,
            'update_time':self.update_time,
            'create_time':self.create_time,
        }


class minority_family_holidays(db.Model,baseModel):
    __tablename__='t_minority_family_holidays'
    id = db.Column(db.Integer, primary_key=True)
    holidays_name=db.Column(db.String(64),unique=True,nullable=False)
    start_time = db.Column(db.Date, default=date.today())
    end_time = db.Column(db.Date, default=date.today())
    comments=db.Column(db.String(255))

    def serialization(self):
        return {
            'id': self.id,
            'holidays_name': self.holidays_name,
            'start_time': self.start_time,
            'end_time':self.end_time,
            'comments':self.comments
        }

class dutyPlan(db.Model,baseModel):
    __tablename__ = 't_duty_plan'
    duty_plan_id = db.Column(db.Integer, primary_key=True)
    duty_plan_date = db.Column(db.Date)
    is_week = db.Column(db.String(64))
    duty_type = db.Column(db.String(64),nullable=False)
    is_working = db.Column(db.Integer,nullable=False)
    comment = db.Column(db.String(256))
    status = db.Column(db.Integer,nullable=False,default=1)
    staff_code = db.Column(db.String(64),db.ForeignKey('t_staff.staff_code'))
    staff = db.relationship('staff', primaryjoin=(staff.staff_code == staff_code))
    duty_place_code = db.Column(db.String(32),db.ForeignKey('t_place.duty_place_code'))
    dutyPlace = db.relationship('dutyPlace', primaryjoin=(dutyPlace.duty_place_code == duty_place_code))

    def serialization(self):
        return {
            'duty_plan_id':self.duty_plan_id,
            'duty_place_code': self.duty_place_code,
            'duty_plan_date': str(self.duty_plan_date),
            'is_week': self.is_week,
            'duty_type': self.duty_type,
            'is_working': self.is_working,
            'status': self.status,
            'comment': self.comment,
            'staff_name': self.check_staff_data(self.staff),
            'duty_place_name': self.check_place_data(self.dutyPlace),
            'update_time': self.update_time,
            'create_time': self.create_time
        }

    def check_staff_data(self,obj):
        if obj is not None:
            return obj.staff_name
        else:
            return None

    def check_place_data(self,obj):
        if obj is not None:
            return obj.duty_place_name
        else:
            return None

class other_setting(db.Model,baseModel):
    __tablename__ = 't_other_setting'
    other_id = db.Column(db.Integer, primary_key=True)
    other_setting_key = db.Column(db.String(64))
    other_setting_value = db.Column(db.String(64))
    is_deleted = db.Column(db.Boolean,default=False,nullable=False)

    def serialization(self):
        return {
            'other_id':self.other_id,
            'other_setting_key': self.other_setting_key,
            'other_setting_value': self.other_setting_value
        }