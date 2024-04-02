from arrange.utils import db
from . import sys_role
from sqlalchemy import and_
# from arrange.utils.redis_utils import

class role_model():

    sysRoleModel = sys_role()
    def get_name_list(self):
        role_list= self.sysRoleModel.query.with_entities(sys_role.role_name).all()
        if len(role_list)>0:
            ls = []
            for role in role_list:
                ls.append(role[0])
            return ls


    def get_role_id_by_name(self,role_name):
        try:
            role_id=self.sysRoleModel.query.with_entities(sys_role.role_id).filter_by(role_name=role_name).first()
            return role_id[0]
        except Exception:
            return 1

    def get_list(self):
        try:
            role_list= self.sysRoleModel.query.with_entities(sys_role.role_id,sys_role.role_name).all()
            return role_list
        except Exception:
            return None

    def get_role_isdisable_list(self):
        roleid_list=self.sysRoleModel.query.filter_by(role_isdisable=1).with_entities(sys_role.role_id).all()
        if roleid_list is not None:
            role_ids=[i[0] for i in roleid_list]
            return role_ids
        else:
            return None


    def add_role(self,role_name):
        role=sys_role(role_name=role_name)
        try:
            db.session.add(role)
            db.session.commit()
            res=1
        except Exception:
            res=0
        return  res

    def delete_role_by_id(self,role_id):
        role=self.sysRoleModel.query.filter_by(role_id=role_id).first()
        if role is not None:
            try:
                db.session.delete(role)
                db.session.commit()
                return 1
            except Exception:
                return 0
        else:
            return 0

    def update_role_by_id(self,role_id,role_name):
        role = self.sysRoleModel.query.filter_by(role_id=role_id).first()
        if role is not None:
            try:
                role.role_name = role_name
                db.session.commit()
                return 1
            except Exception:
                return 0
        else:
            return 0


    def get_role_list(self,offset,limit,keyword):
        if keyword is not None:
            ls=self.sysRoleModel.query.filter(sys_role.role_name.like('%{}%'.format(keyword))).offset(offset).limit(limit).all()
            cnt=self.sysRoleModel.query.filter(sys_role.role_name.like('%{}%'.format(keyword))).count()
        else:
            ls=self.sysRoleModel.query.offset(offset).limit(limit).all()
            cnt=self.sysRoleModel.query.count()
        return ls,cnt


    def updatestatus(self, role_id,isdisable):
        role = self.sysRoleModel.query.filter_by(role_id=role_id).first()
        res = 0
        try:
            if role is not None:
                role.role_isdisable = isdisable
                db.session.commit()
                res=1
        except Exception:
            res = 0
        return res


    def get_role_list_by_disabled(self):
        role_disabled_list=self.sysRoleModel.query.with_entities(sys_role.role_id).filter_by(role_isdisable=0).all()
        res=[]
        try:
            if role_disabled_list is not None or len(role_disabled_list)>0:
                for item in role_disabled_list:
                    res.append(item[0])
        except Exception:
            res=[]
        return res


