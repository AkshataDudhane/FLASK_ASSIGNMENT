from orders_model import OrdersModel
from user_service import User
from flask import *
class Order:
    
    def __init__(self, order_id, name, email, state, zipcode,birthday=None):
        self.order_id = order_id
        self.user=User(name,birthday,email,state,zipcode)

    def validate_order(self):
        validation_checks = [
            (self.user.check_state, "INVALID_STATE", "Invalid state"),
            (self.user.check_zip, "INVALID_ZIPCODE", "Invalid ZipCode"),
            (self.user.val_weekday, "INVALID_WEEKDAY", "Invalid Weekday"),
            (self.user.check_email, "INVALID_EMAIL", "Invalid Email"),
            (self.user.calculateAge, "INVALID_AGE", "Invalid Age")
        ]

        for check_function, error_code, error_message in validation_checks:
            if not check_function():
                return {
                    "error_code": "400",
                    "error": error_code,
                    "message": error_message
                }

        return None
    
    def save_order(self):
        order_model = OrdersModel(name=self.user.name, birthday=self.user.birthday, email=self.user.email, state=self.user.state, zipcode=self.user.zipcode)
        OrdersModel.save(order_model)

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


print("Validation successful")