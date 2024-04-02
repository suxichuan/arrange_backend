from arrange.utils import db
from . import admin
class admin_model():

    def add_admin(self,adminobj):
        try:
            adm=admin(account=adminobj.account,password=adminobj.password,
            name=adminobj.name,nickname=adminobj.nickname,email=adminobj.email,telephone=adminobj.telephone)
            db.session.add(adm)
            db.session.commit()
            return 1
        except Exception as e:
            print(e)
            return None

    def check_exist(self,account):
        try:
            adm = admin.query.filter_by(account=account).first()
            return adm
        except Exception:
            return None

    def find_admin_by_account(self,account):
        try:
            adm = admin.query.filter_by(account=account).first()
            return adm
        except Exception:
            return None

    def find_admin_by_account_and_passwd(self,account,password):
        try:
            adm = admin.query.filter_by(account=account,passwd=password).first()
            return adm
        except Exception:
            return None





