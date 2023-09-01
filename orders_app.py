from mongoengine import connect
from datetime import datetime
from orders_model import OrdersModel
from orders_service import Order
from flask import *
from mongoengine.errors import DoesNotExist


app = Flask(__name__)

connect('OrderDb')

@app.route('/order', methods=['POST'])
def create_order():
    data = request.json

    required_fields = ['name', 'birthday','email', 'state', 'zipcode']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        error_response = {
            "error_code": "400",
            "error": "MISSING_FIELDS",
            "message": f"Missing required fields: {', '.join(missing_fields)}"
        }
        return jsonify(error_response), 400

    if not isinstance(data['name'], str) or len(data['name'])>100:
        error_response = {"error_code": "400", "error": "INVALID_NAME", "message": "Invalid name"}
        return jsonify(error_response), 400
    if len(data['zipcode'])>10:
         error_response = {"error_code": "400", "error": "INVALID ZIP_CODE", "message": "Zipcode not in range"}
         return jsonify(error_response), 400

    try:
        datetime.strptime(data['birthday'], '%m/%d/%Y')
    except ValueError:
            error_response = {"error_code": "400", "error": "INVALID_BIRTHDAY_FORMAT", "message": "Invalid birthday format"}
            return jsonify(error_response), 400

    # Validate input data using Order class methods
    order = Order(order_id=id,name=data['name'], birthday=data.get('birthday'), email=data['email'], state=data['state'], zipcode=data['zipcode']) 
    
    validation_result = order.validate_order()
    if validation_result:
        return jsonify(validation_result), 400
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
    order_dict = order_model.to_dict()

    return jsonify({"message": "order created successfully", "response": order_dict}), 201


@app.route('/order/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        order = OrdersModel.objects(id=str(order_id)).get()
        if not order:
            return jsonify({
        "error_code" : "404",
        "error" : "ORDER_NOT_FOUND",
        "message" : "Order does not exists.",
    }
    ), 404
        
        order.update(set__is_deleted=True, set__del_time=datetime.utcnow())
        
        return jsonify({"is_deleted":order.is_deleted,"message": "Order marked as deleted"}), 200
    except DoesNotExist:
        return jsonify({"error_code": "404", "message": "Order not found", "error": "ORDER_NOT_FOUND"}), 404
   
    except Exception as e:
         return jsonify({"error_code": "500", "message": "Internal Server Error", "error": str(e)}), 500

@app.route('/order/<order_id>', methods=['GET']) #get order by id
def get_order(order_id):
    try:
        order = OrdersModel.objects(id=order_id).first()

        if not order:
            return jsonify({"error_code": "404", "message": "Order is not found", "error": "ORDER_NOT_FOUND"}), 404

        if order.is_deleted:
            return jsonify({"error_code": "404", "message": "Can't fetch deleted order"}), 404

        order_dict = order.to_dict()
        return jsonify({"response": order_dict}), 200

    except DoesNotExist:
        return jsonify({"error_code": "404", "message": "Order not found", "error": "ORDER_NOT_FOUND"}), 404
    except Exception as e:
        # Handle other exceptions, log them, and return an appropriate response.
        return jsonify({"error_code": "500", "message": "Internal Server Error", "error": str(e)}), 500



@app.route('/orders', methods=['GET'])
def list_orders():
    try:
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
        start_index=per_page * (page - 1)
        end_index=per_page * page
        if sort_order == 1:
                orders = query.order_by('created_time')[start_index:end_index]
        elif sort_order == -1:
                orders = query.order_by('-created_time')[start_index:end_index]
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
    except Exception as e:
         return jsonify({"error_code": "500", "message": "Internal Server Error", "error": str(e)}), 500
        

@app.route('/order/<order_id>', methods=['PUT'])
def mark_order_delivered(order_id):
    # Retrieve the order based on the provided order_id
    try:
        order = OrdersModel.objects(id=str(order_id)).get()

        if not order:
            return jsonify({"error": "Order not found"}), 404
        if order.is_delivered:
            return jsonify({"message": "Order is already marked as delivered"}), 400

        # Update the is_delivered field to True
        order.is_delivered = True
        order.save()

        return jsonify({"is_delivered":order.is_delivered,"message": "Order marked as delivered"}), 200
    except Exception as e:
         return jsonify({"error_code": "500", "message": "Internal Server Error", "error": str(e)}), 500
      


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 ,debug=True)