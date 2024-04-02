from arrange.utils import db
from . import sys_status
from sqlalchemy import and_
# from arrange.utils.redis_utils import RedisUtils,get_redis_intance
#


class status_model():

    sysStatusModel=sys_status()

    # def get_status_list(self,status_id,status_name,offset,limit):
    #     try:
    #         if status_name is not None and status_id is not None:
    #             status_list = self.sysStatusModel.query.filter(and_(sys_status.status_name.like('%{}%'.format(status_name)),sys_status.status_id.like('%{}%'.format(status_id)))).offset(offset).limit(limit).all()
    #             status_count=self.sysStatusModel.query.filter(and_(sys_status.status_name.like('%{}%'.format(status_name)),sys_status.status_id.like('%{}%'.format(status_id)))).count()
    #             return (status_list,status_count)
    #         if  status_id is not  None:
    #             status_list = self.sysStatusModel.query.filter(sys_status.status_id.like('%{}%'.format(status_id))).offset(offset).limit(limit).all()
    #             status_count = self.sysStatusModel.query.filter(sys_status.status_id.like('%{}%'.format(status_id))).count()
    #             return (status_list,status_count)
    #         if status_name is not None:
    #             status_list = self.sysStatusModel.query.filter(sys_status.status_name.like('%{}%'.format(status_name))).offset(offset).limit(limit).all()
    #             status_count = self.sysStatusModel.query.filter(sys_status.status_name.like('%{}%'.format(status_name))).count()
    #             return (status_list,status_count)
    #         if status_name is None and status_id is None:
    #             status_list = self.sysStatusModel.query.offset(offset).limit(limit).all()
    #             status_count = self.sysStatusModel.query.count()
    #             return (status_list,status_count)
    #     except Exception:
    #         return (None,0)

    # def get_name_list(self):
    #     try:
    #         redisutils = get_redis_intance()
    #         status_ls=redisutils.get('statuslist:1')
    #         if status_ls is not None:
    #             return status_ls
    #         else:
    #             status_list= self.sysStatusModel.query.with_entities(sys_status.status_name).all()
    #             if len(status_list)>0:
    #                 ls = []
    #                 for status in status_list:
    #                     ls.append(status[0])
    #                 redisutils.set('statuslist:1', ls)
    #                 return ls
    #     except Exception as e:
    #         return None

    def get_name_list(self):
        try:
            status_list= self.sysStatusModel.query.with_entities(sys_status.status_name).all()
            if len(status_list)>0:
                ls = []
                for status in status_list:
                    ls.append(status[0])
                return ls
        except Exception as e:
            return None

    def get_status_id_by_name(self,status_name):
        try:
            status_id=self.sysStatusModel.query.with_entities(sys_status.status_id).filter_by(status_name=status_name).first()
            return status_id[0]
        except Exception as e:
            return 1

    def get_list(self):
        try:
            status_list= self.sysStatusModel.query.with_entities(sys_status.status_id,sys_status.status_name).all()
            return status_list
        except Exception as e:
            return None

    def get_status_isdisable_list(self):
        statusid_list = self.sysStatusModel.query.filter_by(status_isdisable=1).with_entities(sys_status.status_id).all()
        if statusid_list is not None:
            status_ids=[i[0] for i in statusid_list]
            return status_ids
        else:
            return None

    def get_status_lists(self,offset,limit,keyword):
        if keyword is not None:
            ls=self.sysStatusModel.query.filter(sys_status.status_name.like('%{}%'.format(keyword))).offset(offset).limit(limit).all()
            cnt=self.sysStatusModel.query.filter(sys_status.status_name.like('%{}%'.format(keyword))).count()
        else:
            ls=self.sysStatusModel.query.offset(offset).limit(limit).all()
            cnt=self.sysStatusModel.query.count()
        return ls,cnt

    def update_status_by_id(self,status_id,status_name):
        status = self.sysStatusModel.query.filter_by(status_id=status_id).first()
        if status is not None:
            try:
                status.status_name = status_name
                db.session.commit()
                return 1
            except Exception:
                return 0
        else:
            return 0

    def delete_status_by_id(self,status_id):
        status=self.sysStatusModel.query.filter_by(status_id=status_id).first()
        if status is not None:
            try:
                db.session.delete(status)
                db.session.commit()
                return 1
            except Exception:
                return 0
        else:
            return 0

    def add_status(self,status_name):
        status=sys_status(status_name=status_name)
        try:
            db.session.add(status)
            db.session.commit()
            # redisutils=get_redis_intance()
            # redisutils.delete('statuslist:1')
            res=1
        except Exception:
            res=0
        return  res


    def updatestatus(self, status_id,isdisable):
        status = self.sysStatusModel.query.filter_by(status_id=status_id).first()
        res = 0
        try:
            if status is not None:
                status.status_isdisable = isdisable
                db.session.commit()
                # redisutils = get_redis_intance()
                # redisutils.delete('statuslist:1')
                res=1
        except Exception:
            res = 0
        return res


    def get_status_disabled_list(self):
        status_disabled_list=self.sysStatusModel.query.with_entities(sys_status.status_id).filter_by(status_isdisable=0).all()
        res=[]
        try:
            if status_disabled_list is not None or len(status_disabled_list)>0:
             for item in status_disabled_list:
                res.append(item[0])
        except Exception:
            res=[]
        return res



