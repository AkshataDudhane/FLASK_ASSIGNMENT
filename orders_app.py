from flask import *
from mongoengine import connect
from datetime import datetime
from orders_model import OrdersModel
from orders_service import Order

app = Flask(__name__)

connect('OrderDb')

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json
    
    # Validate input data using Order class methods
    order = Order(order_id=id,name=data['name'], birthday=data['birthday'], email=data['email'], state=data['state'], zipcode=data['zipcode']) 
    if not order.user.check_state():
        error_response = {"error_code": "400", "error": "INVALID_STATE", "message": "Invalid state"}
        return jsonify(error_response), 400
    if not order.user.check_zip():
        error_response = {"error_code": "400", "error": "INVALID_ZIPCODE", "message": "Invalid ZipCode"}
        return jsonify(error_response), 400
    if not order.user.val_weekday():
        error_response = {"error_code": "400", "error": "INVALID_WEEKDAY", "message": "Invalid Weekday"}
        return jsonify(error_response), 400
    if not order.user.check_email():
        error_response = {"error_code": "400", "error": "INVALID_EMAIL", "message": "Invalid Email"}
        return jsonify(error_response), 400
    if not order.user.calculateAge():
        error_response = {"error_code": "400", "error": "INVALID_AGE", "message": "Invalid Age"}
        return jsonify(error_response), 400
    # Create a new OrdersModel instance
    order_model = OrdersModel(
        name=order.user.name,
        birthday=order.user.birthday,
        email=order.user.email,
        state=order.user.state,
        zipcode=order.user.zipcode
    )

    # Save the order to the database
    order_model.save()
    # Prepare the response data
    response_data = {
        # "order_id": order.order_id,
        "name": order.user.name,
        "email": order.user.email,
        "birthday": order.user.birthday,
        "state": order.user.state,
        "zipcode": order.user.zipcode,
        "created_time": order_model.created_time,
        "updated_time": order_model.updated_time,
        "is_delivered": False
    }

    # success_response = {"data": response_data, "success": True}
    return jsonify({"message":"order created successfully","order_id":str(order_model.id),"response":response_data}), 201

@app.route('/order/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = OrdersModel.objects(id=order_id).first()
    if not order:
        return jsonify({
       "error_code" : "404",
       "error" : "ORDER_NOT_FOUND",
       "message" : "Order does not exists.",
}
), 404
    
    order.update(set__is_deleted=True, set__del_time=datetime.utcnow())
    
    return jsonify({"is_deleted":bool(order.is_deleted),"message": "Order marked as deleted"}), 200

@app.route('/order/<order_id>', methods=['GET']) #get order by id
def get_order(order_id):
    order = OrdersModel.objects(id=order_id).first()
    
    if not order:
        return jsonify({"error_code":"400","message":"Order does not exists","error": "ORDER_NOT_FOUND"}), 404
    
    response_data = {
        "order_id":str(order.id),
        "user_name": order.name,
        "email": order.email,
        "birthday": order.birthday,
        "state": order.state,
        "zipcode": order.zipcode,
        "created_time": order.created_time,
        "updated_time": order.updated_time,
        "is_delivered": order.is_delivered,
        "is_deleted": order.is_deleted
        
    }

    return jsonify({"response":response_data}), 200


@app.route('/orders', methods=['GET'])
def list_orders():
    page = int(request.args.get('page', 1))
    per_page = 10
    filter_email = request.args.get('email')
    filter_state = request.args.get('state')
    filter_zipcode = request.args.get('zipcode')
    sort_order = int(request.args.get('sort_order', 1))  # 1 for ascending, -1 for descending

    query = OrdersModel.objects(is_deleted=False)

    if filter_email:
        query = query.filter(email=filter_email)
    if filter_state:
        query = query.filter(state=filter_state)
    if filter_zipcode:
        query = query.filter(zipcode=filter_zipcode)

    total_orders = query.count()
    orders = query.order_by(sort_order * 'created_time')[per_page * (page - 1):per_page * page]

    if not orders:
        return jsonify({"message": "No orders found"}), 200

    orders_list = []
    for order in orders:
        order_data = {
            "order_id":str(order.id),
            "user_name": order.name,
            "email": order.email,
            "birthday": order.birthday,
            "state": order.state,
            "zipcode": order.zipcode,
            "created_time": order.created_time,
            "updated_time": order.updated_time,
            "is_delivered": order.is_delivered
        }
        orders_list.append(order_data)

    response_data = {
        "orders": orders_list,
        "total_orders": total_orders,
        "page": page,
        "per_page": per_page
    }

    return jsonify(response_data), 200


@app.route('/order/<order_id>', methods=['PUT'])
def mark_order_delivered(order_id):
    # Retrieve the order based on the provided order_id
    order = OrdersModel.objects(id=order_id).first()

    if not order:
        return jsonify({"error": "Order not found"}), 404

    # Update the is_delivered field to True
    order.is_delivered = True
    order.save()

    return jsonify({"is_delivered":order.is_delivered,"message": "Order marked as delivered"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)