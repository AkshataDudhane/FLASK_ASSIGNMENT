from mongoengine import *
import datetime 
connect('OrderDb')
class OrdersModel(Document):
    
    name = StringField(required=True)
    birthday = DateTimeField(required=True)
    email = StringField(required=True)
    state = StringField(required=True)
    zipcode = StringField(required=True)
    is_deleted = BooleanField(default=False)
    del_time=DateTimeField(default=None)
    created_time = DateTimeField(default=datetime.datetime.utcnow)
    updated_time = DateTimeField(default=datetime.datetime.utcnow)
    is_delivered = BooleanField(default=False)

    def to_dict(self):
        response_data = {
            "name": self.name,
            "email": self.email,
            "birthday": self.birthday,
            "state": self.state,
            "zipcode": self.zipcode,
            "created_time": self.created_time,
            "updated_time": self.updated_time,
            "is_delivered": self.is_delivered
        }
        return response_data