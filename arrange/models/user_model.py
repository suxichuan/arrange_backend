from . import user
from arrange.utils import db

class usermodel():
    def check_exist(username):
        try:
            usr = user.query.filter_by(username=username).first()
            return usr
        except Exception:
            return None

    def add_user(self,user_data):
        data=user(username=user_data.username,password=user_data.password,email=user_data.email,phone=user_data.phone,nickname=user_data.nickname)
        db.session.add(data)
        db.session.commit()