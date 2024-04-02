from arrange.utils import db
from . import dutyPlace;
from sqlalchemy import and_

class place_duty_model():
    placeModel = dutyPlace()

    def get_place_list(self, offset, limit,place_name,place_code):
        try:
            if place_name is not None and place_code is not None:
                place_list = self.placeModel.query.filter(and_(dutyPlace.duty_place_name.like('%{}%'.format(place_name)),dutyPlace.duty_place_code.like('%{}%'.format(place_code)),dutyPlace.is_deleted==0)).offset(offset).limit(limit).all()
                place_count=self.placeModel.query.filter(and_(dutyPlace.duty_place_name.like('%{}%'.format(place_name)),dutyPlace.duty_place_code.like('%{}%'.format(place_code)),dutyPlace.is_deleted==0)).count()
                return (place_list,place_count)
            if  place_code is not  None:
                place_list = self.placeModel.query.filter(and_(dutyPlace.duty_place_code.like('%{}%'.format(place_code)),dutyPlace.is_deleted==0)).offset(offset).limit(limit).all()
                place_count = self.placeModel.query.filter(and_(dutyPlace.duty_place_code.like('%{}%'.format(place_code)),dutyPlace.is_deleted==0)).count()
                return (place_list, place_count)
            if place_name is not None:
                place_list = self.placeModel.query.filter(and_(dutyPlace.duty_place_name.like('%{}%'.format(place_name)),dutyPlace.is_deleted==0)).offset(offset).limit(limit).all()
                place_count = self.placeModel.query.filter(and_(dutyPlace.duty_place_name.like('%{}%'.format(place_name)),dutyPlace.is_deleted==0)).count()
                return (place_list, place_count)
            if place_name is None and place_code is None:
                place_list = self.placeModel.query.filter_by(is_deleted=0).offset(offset).limit(limit).all()
                place_count = self.placeModel.query.filter_by(is_deleted=0).count()
                return (place_list, place_count)
        except Exception:
            return (None,0)

    def updatestatus(self, place_code,update_status):
        place = self.placeModel.query.filter_by(duty_place_code=place_code).first()
        res = 0
        try:
            if place is not None:
                place.duty_place_status = update_status
                db.session.commit()
                res=1
        except Exception:
            res = 0
        return res

    def delete_place(self,place_code):
        place=self.placeModel.query.filter_by(duty_place_code=place_code).first()
        res=0
        if place is not None:
            try:
                place.is_deleted=1
                db.session.commit()
                res=1
            except Exception:
                res=0

        return res

    def update_place(self,place_code,place_name,place_num):
        place=self.placeModel.query.filter_by(duty_place_code=place_code).first()
        res=0
        if place is not  None:
            try:
                place.duty_place_name=place_name
                place.duty_place_num=place_num
                db.session.commit()
                res=1
                return res
            except Exception:
                res=0
        return res

    def add(self,place_code,place_name,duty_place_num):
        place=dutyPlace(duty_place_code=place_code,
                        duty_place_name=place_name,duty_place_status='1',duty_place_num=duty_place_num)
        res=0
        try:
            db.session.add(place)
            db.session.commit()
            res=1
        except Exception:
            res=0
        return res

    def check_code(self,place_code):
        place = self.placeModel.query.filter_by(duty_place_code=place_code).first()
        res = 0
        if place is not None:
            res=1
            return res
        return res


    def get_place_list_by_status(self):
        place_list=self.placeModel.query.filter(and_(dutyPlace.duty_place_status==1,dutyPlace.is_deleted==0)).with_entities(dutyPlace.duty_place_code,dutyPlace.duty_place_num).all()
        if place_list is not None:
            place_config=[{'place_code':i[0],'num':i[1]} for i in place_list]
            return place_config
        else:
            return []




