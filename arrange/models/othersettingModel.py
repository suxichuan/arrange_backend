from arrange.utils import db
from . import other_setting
from sqlalchemy import and_


class other_model():

    othersettingModel = other_setting()


    def delete_setting_by_id(self,setting_id):
        setting=self.othersettingModel.query.filter_by(other_id=setting_id).first()
        if setting is not None:
            try:
                setting.is_deleted=1
                db.session.commit()
                return 1
            except Exception:
                return 0
        else:
            return 0

    def update_setting_by_id(self,setting_id,other_setting_key,other_setting_value):
        other_setting = self.othersettingModel.query.filter_by(other_id=setting_id).first()
        if other_setting is not None:
            try:
                other_setting.other_setting_key = other_setting_key
                other_setting.other_setting_value = other_setting_value
                db.session.commit()
                return 1
            except Exception:
                return 0
        else:
            return 0


    def get_setting_list(self,offset,limit,keyword):
        if keyword is not None:
            ls=self.othersettingModel.query.filter(and_(other_setting.other_setting_key.like('%{}%'.format(keyword)),other_setting.is_deleted==0)).offset(offset).limit(limit).all()
            cnt=self.othersettingModel.query.filter(and_(other_setting.other_setting_key.like('%{}%'.format(keyword)),other_setting.is_deleted==0)).count()
        else:
            ls=self.othersettingModel.query.filter_by(is_deleted=0).offset(offset).limit(limit).all()
            cnt=self.othersettingModel.query.filter_by(is_deleted=0).count()
        return ls,cnt




