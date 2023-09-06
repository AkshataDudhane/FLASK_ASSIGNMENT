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


    def mark_order_delivered(self, order_id):
            order = OrdersModel.objects(id=order_id).first()

            if not order:
                return {"error": "Order not found"}, 404
            if order.is_delivered:
                return {"message": "Order is already marked as delivered"}, 400

            # Update the is_delivered field to True
            order.is_delivered = True
            order.save()

            return {"is_delivered": order.is_delivered, "message": "Order marked as delivered"}, 200

