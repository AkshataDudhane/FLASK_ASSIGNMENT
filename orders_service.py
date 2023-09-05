from orders_model import OrdersModel
from user_service import User
from flask import *
from datetime import datetime
from mongoengine.errors import DoesNotExist

class Order:
    
    def __init__(self, order_id, name, email, state, zipcode,birthday=None):
        self.order_id = order_id
        self.user=User(name,birthday,email,state,zipcode)
        self.created_time = datetime.utcnow()  # Define your created_time
        self.updated_time = datetime.utcnow() 
        self.is_delivered = False

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
        order_model.save()

    def to_dict(self):
        response_data = {
            "name": self.user.name,
            "email": self.user.email,
            "birthday": self.user.birthday,
            "state": self.user.state,
            "zipcode": self.user.zipcode,
            "created_time": self.created_time,
            "updated_time": self.updated_time,
            "is_delivered": self.is_delivered
        }
        return response_data
    
    def delete_order(order_id):
        try:
            order = OrdersModel.objects(id=str(order_id)).get()
            if not order:
                return None, 404

            order.update(set__is_deleted=True, set__del_time=datetime.utcnow())

            return {"is_deleted":order.is_deleted,"message": "Order marked as deleted"}, 200
        except DoesNotExist:
            return {"error_code": "404", "message": "Order not found", "error": "ORDER_NOT_FOUND"}, 404
        except Exception as e:
            return {"error_code": "500", "message": "Internal Server Error", "error": str(e)}, 500
    def get_order(order_id):
        try:
            order = OrdersModel.objects(id=order_id).first()

            if not order:
                return {
                    "error_code": "404",
                    "message": "Order not found",
                    "error": "ORDER_NOT_FOUND"
                }, 404

            if order.is_deleted:
                return {
                    "error_code": "404",
                    "message": "Can't fetch deleted order"
                }, 404

            order_dict = order.to_dict()
            return {"response": order_dict}, 200

        except DoesNotExist:
            return {
                "error_code": "404",
                "message": "Order not found",
                "error": "ORDER_NOT_FOUND"
            }, 404
        except Exception as e:
            # Handle other exceptions, log them, and return an appropriate response.
            return {
                "error_code": "500",
                "message": "Internal Server Error",
                "error": str(e)
            }, 500

    def list_orders(page, per_page, filter_email, filter_state, filter_zipcode, sort_order):
        try:
            query = OrdersModel.objects(is_deleted=False)

            if filter_email:
                query = query.filter(email=filter_email)
            if filter_state:
                query = query.filter(state=filter_state)

            if filter_zipcode:
                query = query.filter(zipcode=filter_zipcode)
            total_orders = query.count()
            start_index = per_page * (page - 1)
            end_index = per_page * page
            if sort_order == 1:
                orders = query.order_by('created_time')[start_index:end_index]
            elif sort_order == -1:
                orders = query.order_by('-created_time')[start_index:end_index]
            if not orders:
                return {"message": "No orders found"}, 200

            orders_list = []

            for order in orders:
                order_dict = order.to_dict()
                orders_list.append(order_dict)

            response_data = {
                "orders": orders_list,
                "total_orders": total_orders,
                "page": page,
                "per_page": per_page
            }

            return response_data, 200
        except Exception as e:
            return {"error_code": "500", "message": "Internal Server Error", "error": str(e)}, 500
print("Validation successful")