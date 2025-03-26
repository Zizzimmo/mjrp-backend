from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from mjrp import calculate_cost  # Assuming calculate_cost function is defined in mjrp module
from flask_talisman import Talisman
import os

app = Flask(__name__)
CORS(app)
Talisman(app, content_security_policy=None)

# Serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Serve index.html for root URL
@app.route('/')
def index():
    return render_template('index.html')

def get_array_lengths(data):
    # Initialize lengths
    buyer_num = len(data)
    item_num = len(data[0]['itemsData']) if data else 0  # Assuming all items have 'itemsData'

    return buyer_num, item_num

def extract_data(item):
    demand = item.get('demand', 0)
    price = item.get('price', 0.0)
    frequency = item.get('frequency', 1)
    minor_setup_cost = item.get('minorSetupCost', 0.0)
    # inventory_carrying_charge = item.get('inventoryCarryingCharge', 0.0)
    # print(price)
    return demand, price, frequency, minor_setup_cost

def extract_info(info):
    major_setup_cost = info.get('majorSetupCost')
    inventory_carrying_charge = info.get('inventoryCarryingCharge')
    return major_setup_cost, inventory_carrying_charge

# @app.route('/calculate', methods=['POST'])
# def calculate():
#     data = request.get_json()
#     print("Received data:", data)
#     if not data or not isinstance(data, list):
#         return jsonify({"error": "Invalid JSON data provided. Expected a list of items."}), 400

#     results = []
#     buyer_num, item_num = get_array_lengths(data)
#     print("Buyer num:", buyer_num)
#     print("Item num:", item_num)
#     for item in data:
#         if 'buyerInfo' not in item or 'itemsData' not in item:
#             results.append({"error": "Invalid JSON structure for an item."})
#             continue

#         buyer_info = item['buyerInfo']
#         items_data = item['itemsData']
#         print("Buyer info:", buyer_info)
#         print("Items data:", items_data)

#         # Extracting relevant parameters from buyer_info and items_data
#         try:
#             demand = [int(data.get('demand', 0)) for data in items_data]  
#             purchasing_cost = [float(data.get('price', 0.0)) for data in items_data]  
#             major_setup_cost = float(buyer_info.get('majorSetupCost0', 0.0))  
#             time_multipliers = [int(data.get('frequency', 1)) for data in items_data]  
#             minor_setup_cost = [float(data.get('minorSetupCost', 0.0)) for data in items_data]  
#             variable_cost = [float(data.get('inventoryCarryingCharge', 0.0)) for data in items_data]  

#             print(demand)
#             print(purchasing_cost)
#             print(major_setup_cost)
#             print(time_multipliers)
#             print(minor_setup_cost)
#             print(variable_cost)

#             # Ensure none of the extracted values are None
#             if None in demand or None in purchasing_cost or None in time_multipliers \
#                     or None in minor_setup_cost or None in variable_cost:
#                 raise ValueError("Invalid value detected. NoneType encountered.")

#             # Call the calculate_cost function with the extracted parameters
#             result = calculate_cost({
#                 'Demand': demand,
#                 'price': purchasing_cost,  # Ensure the key matches the expected parameter name
#                 'Major Setup Cost': major_setup_cost,
#                 'frequency': time_multipliers,  # Ensure the key matches the expected parameter name
#                 'Minor Setup Cost': minor_setup_cost,
#                 'inventoryCarryingCharge': variable_cost  # Ensure the key matches the expected parameter name
#             }, buyer_num, item_num)
            
#             results.append(result)
#         except Exception as e:
#             results.append({"error": str(e)})
    
#     return jsonify(results), 200
@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    print(data)
    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid JSON data provided. Expected a list of items."}), 400

    results = []
    buyer_demand_lists = []
    buyer_price_lists = []
    buyer_frequency_lists = []
    # buyer_inventory_carrying_charge_lists = []
    buyer_minor_setup_cost_lists = []
    buyer_num, item_num = get_array_lengths(data)
    print("Buyer num:", buyer_num)
    print("Item num:", item_num)
    
    for buyer_data in data:
        buyer_info = buyer_data.get('buyerInfo', {})
        items_data = buyer_data.get('itemsData', [])
        
        if not buyer_info:
            results.append({"error": "Buyer info not provided."})
            continue
        buyer_demand_list = []
        buyer_price_list = []
        buyer_frequency_list = []
        buyer_minor_setup_cost_list = []
        # buyer_inventory_carrying_charge_list = []
        major_setup_cost, inventory_carrying_charge = extract_info(buyer_info)
        # print("major Setup Cost:", major_setup_cost)
        # print("inventory Carrying Charge:", inventory_carrying_charge)

        for item in items_data:
            demand, price, frequency, minor_setup_cost = extract_data(item)

            buyer_demand_list.append(demand)
            buyer_price_list.append(price)
            buyer_frequency_list.append(frequency)
            buyer_minor_setup_cost_list.append(minor_setup_cost)
        
        buyer_demand_lists.append(buyer_demand_list)
        buyer_frequency_lists.append(buyer_frequency_list)
        buyer_price_lists.append(buyer_price_list)
        buyer_minor_setup_cost_lists.append(buyer_minor_setup_cost_list)
        
    print("demand array:", buyer_demand_lists)
    print("frequency array: ", buyer_frequency_lists)
    print("price array:", buyer_price_lists)
    print("minor setup cost: ", buyer_minor_setup_cost_lists)
    # print("inventory carrying charge:", buyer_inventory_carrying_charge_lists)
    try:
        # Assuming the rest of your calculation logic goes here
        # Call the calculate_cost function with the extracted parameters
        result = calculate_cost({
            'demand': buyer_demand_lists,
            'price': buyer_price_lists,
            'frequency': buyer_frequency_lists,
            'minorSetupCost': buyer_minor_setup_cost_lists
        }, buyer_num, item_num, major_setup_cost, inventory_carrying_charge)

        results.append(result)
    except Exception as e:
        results.append({"error": str(e)})
    
    return jsonify(results), 200

if __name__ == '__main__':
    # Production Deployment
    app.run(host='0.0.0.0', port=5000)  # Use appropriate port for production
