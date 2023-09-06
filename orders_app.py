from mongoengine import connect
from datetime import datetime
from orders_model import OrdersModel
from orders_service import Order
from flask import *


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
    order_service = Order(order_id=id,name=data['name'], birthday=data.get('birthday'), email=data['email'], state=data['state'], zipcode=data['zipcode']) 
    
    validation_result = order_service.validate_order()
    if validation_result:
        return jsonify(validation_result), 400

    order_service.save_order()
    order_dict = order_service.to_dict()

    return jsonify({"message": "order created successfully", "response": order_dict}), 201


@app.route('/order/<order_id>', methods=['DELETE'])
def delete_order_route(order_id):
    response_data, status_code = Order.delete_order(order_id)
    if response_data is None:
        return jsonify({
            "error_code": "404",
            "message": "Order not found",
            "error": "ORDER_NOT_FOUND"
        }), 404
    return jsonify(response_data), status_code


@app.route('/order/<order_id>', methods=['GET'])
def get_order_route(order_id):
    response_data, status_code = Order.get_order(order_id)
    if response_data is None:
        return jsonify({
            "error_code": "404",
            "message": "Order not found",
            "error": "ORDER_NOT_FOUND"
        }), 404
    return jsonify({"response": response_data}), status_code



@app.route('/orders', methods=['GET'])
def list_orders_route():
    try:
        page = int(request.args.get('page', 1))
        per_page = 10
        filter_email = request.args.get('email')
        filter_state = request.args.get('state')
        filter_zipcode = request.args.get('zipcode')
        sort_order = int(request.args.get('sort_order', 1))

        response_data, status_code = Order.list_orders(
            page, per_page, filter_email, filter_state, filter_zipcode, sort_order
        )

        return jsonify(response_data), status_code

    except Exception as e:
        return jsonify({"error_code": "500", "message": "Internal Server Error", "error": str(e)}), 500

@app.route('/order/<order_id>', methods=['PUT'])
def mark_orderas_delivered(order_id):
    try:
        order_service = OrdersModel()

        response, status_code = order_service.mark_order_delivered(order_id)

        return jsonify(response), status_code

    except Exception as e:
        return jsonify({"error_code": "500", "message": "Internal Server Error", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000 ,debug=True)