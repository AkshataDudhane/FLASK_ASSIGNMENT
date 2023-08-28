from datetime import datetime
import csv
from mongoengine import *
from mongoengine import connect
from orders_model import OrdersModel
from orders_service import Order

class AcmewinesOrder:
    def read_csv_and_save_to_mongodb(self):
        with open('orders.csv', 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                order_id=row['ID']
                name = row['Name']
                birthday = datetime.strptime(row['Birthday'], '%m/%d/%Y')
                email = row['Email']
                state = row['State']
                zipcode = row['ZipCode']

                order=Order(order_id,name,birthday,email,state,zipcode)
                order.save_order()

    def process_orders(self):
        order=OrdersModel.objects

        for cur_order in order:
            up_order=Order(cur_order.order_id,cur_order.name,cur_order.birthday,cur_order.email,cur_order.state,cur_order.zipcode)
            up_order.mark_order_as_valid()


print("Analyzed successfully")

if __name__ == '__main__':
    connect('OrderDb')
    acmewines_order = AcmewinesOrder()
    acmewines_order.read_csv_and_save_to_mongodb()
    acmewines_order.process_orders()