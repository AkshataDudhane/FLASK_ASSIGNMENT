from orders_model import OrdersModel
from user_service import User
class Order:
    
    def __init__(self, order_id, name,birthday, email, state, zipcode):
        self.order_id = order_id
        self.user=User(name,birthday,email,state,zipcode)

    def validate_order(self):
        valid=(self.user.check_state() & self.user.check_zip() & self.user.val_weekday() & self.user.check_email() & self.user.calculateAge())
        return valid
    
    def save_order(self):
        order_model = OrdersModel(id=self.order_id, name=self.user.name, birthday=self.user.birthday, email=self.user.email, state=self.user.state, zipcode=self.user.zipcode)
        OrdersModel.save(order_model)

    def mark_order_as_valid(self):
        if(self.validate_order()):
            OrdersModel.objects(order_id=self.order_id).update(set__is_valid=True)

print("Validation successful")