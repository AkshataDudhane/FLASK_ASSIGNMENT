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
