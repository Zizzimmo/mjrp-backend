import math

# Define parameters
# item_num = 6
# buyer_num = 2


class Parent:
    def __init__(self, demand, buyer_num, item_num, purchasing_cost, time_multipliers, major_setup_cost, minor_setup_cost, variable_cost):
        self.buyer_num = buyer_num
        self.demand = demand
        self.item_num = item_num
        self.v = purchasing_cost
        self.k = time_multipliers
        self.S = major_setup_cost
        self.s = minor_setup_cost
        self.r = variable_cost
   
    # Function to compute cycle time
    def cycle_time(self, k, t):
        T = k * t
        return T
    
    # Function to compute order quantity
    def order_quantity(self, demand, T):
        Q = []
        for i in range(self.buyer_num):
            buyer_demand = []
            for j in range(self.item_num):
                buyer_demand.append(T * demand[i][j])
            Q.append(buyer_demand)
        return Q
    
    # Function to compute holding cost
    def holding_cost(self, Q, v, r):
        total_holding_cost = 0
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                if isinstance(r, list):
                    total_holding_cost += (Q[i][j] * v[j] * r[j]) / 2
                else:
                    total_holding_cost += (Q[i][j] * v[j] * r) / 2
        return total_holding_cost
    
    # Function to compute setup costs
    def set_up_costs(self, k, T):
        cons = self.S / T
        set_up_array = []
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                set_up_cost = self.s[i][j] / (self.k[i][j] * T)
                set_up_array.append(set_up_cost)
        total_set_up_cost = cons + sum(set_up_array)
        return total_set_up_cost
    
    # Function to compute total annual cost
    def total_annual_cost(self, Q, T):
        total_holding_cost = self.holding_cost(Q, v, r)
        total_setup_cost = self.set_up_costs(Q, T)
        return total_holding_cost + total_setup_cost
    
    # Rand Algorithm
    def rand_algorithm(self, demand, k):
        # Step 1: Initialize parameters
        t_max = self.find_cycle_time_max()
        t_min = self.find_cycle_time_min()

        # Step 2: Initialize variables
        T_p = t_min  # Start with the minimum cycle time
        q = 0  # Initialize iteration counter
        converged = False

        # Step 3: Iterate until convergence
        while not converged:
            # Step 4: Compute k_ijq
            k_ijq = self.compute_k_ijq(T_p, q, demand)

            # Step 6: Compute new cycle time T_p
            T_p = self.compute_new_cycle_time(k_ijq)

            # Step 7: Check for convergence
            if q == 1 or self.not_condition_met(k_ijq):
                q += 1
            else:
                converged = True

        return T_p, k_ijq
    
    # Function to compute k_ijq
    def compute_k_ijq(self, T_p, q, demand):
        k_ijq = []
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                k_ijq.append(2 * self.s[i][j] * T_p**2 / math.sqrt(self.r[j] * self.demand[i][j] * self.v[i]))
        return k_ijq

    # Function to compute new cycle time T_p
    def compute_new_cycle_time(self, k_ijq):
        numerator = 2 * self.S
        denominator = sum(k_ijq)
        T_p = math.sqrt(numerator / denominator)
        return T_p

# Function to check condition for Step 7
    def not_condition_met(k_ijq):
        # Check if kp_ijq - kp_ijq-1 = 1 for any i and j
        # If condition is met, return True; otherwise, return False
        # Implementation depends on specific condition in your problem
        return False

# Helper functions and functions for finding t_max and t_min (to be implemented)
    def func1(self, item_num, buyer_num, s, S):
        set_up_array = []
        for i in range(buyer_num):
            for j in range(item_num):
                set_up_array.append(s[i][j])
        return S + sum(set_up_array)
    
    def func2(self, item_num, buyer_num, d, v, r):
        demand_array = []
        for i in range(buyer_num):
            for j in range(item_num):
                demand_array.append(d[i][j] * v[j])
        return sum([r[j] * demand_array[j] for j in range(len(r))])

    # functions to find tmax
    def find_cycle_time_max(self):
        var_1 = self.func1(self.item_num, self.buyer_num, self.s, self.S)
        var_2 = self.func2(self.item_num, self.buyer_num, self.demand, self.v, self.r)
        T_max = math.sqrt((2 * var_1)/var_2)
        return round(T_max)

    #functions to find Tmin
    # helper functions for tmin
    def t1_helper_function(self, s, r, d, v):
        t1_array = []
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                t_variable = math.sqrt((2 * s) / (r * d * v))
                t1_array.append(t_variable)
                return min(t1_array)

# code for finding the minimum cycle time
    def find_t1(self, s, r, demand, v):
        t1_min = float('inf')
    
        # iteration over all elements of the demand matrix
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                expr = math.sqrt((2 * s[i][j]) / (r[j] * demand[i][j] * v[i]))
                t1_min = min(t1_min, expr)
    
        return t1_min
            
    def func_min1(self, s, k, buyer_num, item_num, S, t1):
        array1 = []
        for i in range(buyer_num):
            for j in range(item_num):
                set_up_cost = s[i][j]/(k[i][j] * t1)
                array1.append(set_up_cost)
        return S + sum(array1)

    def func_min2(self, d, v, k, r, buyer_num, item_num, t1):
        array2 = []
        for i in range(buyer_num):
            for j in range(item_num):
                demand_cost = d[i][j] * v[i] / k[i][j] * t1
                array2.append(demand_cost)
        return sum([r[i] * array2[i] for i in range(len(r))])

    def find_cycle_time_min(self):
        t1 = self.find_t1(self.s, self.r, self.demand, self.v)
        var_1 = self.func_min1(self.s, self.k, self.buyer_num, self.item_num, self.S, t1)
        var_2 = self.func_min2(self.demand, self.v, self.k, self.r, self.buyer_num, self.item_num, t1)
        Tmin = math.sqrt((2 * var_1)/ var_2)
        return round(Tmin)
    
    def get_array_lengths(data):
        buyer_num = len(data)
        try:
            item_num = len(data[0]['itemsData']) if data else 0
        except Exception as e:
            print("Error:", e)
            print("Data:", data)
            item_num = 0
        return buyer_num, item_num


# Given parameters
# S = 1000	# Major setup cost
# s = [[350, 300, 320, 400, 400, 300], [250, 200, 300, 420, 450, 400]]  # Minor setup cost when item i is included in a group replenishment in buyer j
# v = [50, 50, 50, 50, 50, 50]  # Unit variable cost of item i
# r = [5, 5, 5, 5, 5, 5]  # Inventory carrying charge per unit time
# demand = [[10000, 5000, 3000, 1000, 600, 200], [8000, 1000, 12000, 6000, 4500, 100]]	#demand per unit time
# k_ij = [[2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2]] 


    

def calculate_cost(parameters,  buyer_num, item_num ):

    demand = parameters.get('Demand', [])
    purchasing_cost = parameters.get('price', [])
    time_multipliers = parameters.get('frequency', [])
    major_setup_cost = parameters.get('Major Setup Cost', 0.0)
    variable_cost = parameters.get('inventoryCarryingCharge', [])
    minor_setup_cost = parameters.get('Minor Setup Cost', [])

    # Check if all required parameters are extracted and of the correct type
    if demand is None or purchasing_cost is None or time_multipliers is None or major_setup_cost is None or variable_cost is None:
        return {"error": "Required parameters not provided"}

    # Ensure that the parameters are of the expected type (e.g., list)
    if not isinstance(demand, list) or not isinstance(purchasing_cost, list) \
            or not isinstance(time_multipliers, list) or not isinstance(variable_cost, list):
        return {"error": "Parameters must be provided as lists"}
    parent_instance = Parent(demand, buyer_num, item_num, purchasing_cost, time_multipliers, major_setup_cost, minor_setup_cost, variable_cost)

    T_p, k_ijq = parent_instance.rand_algorithm(demand, time_multipliers)
    Q = parent_instance.order_quantity(demand, T_p)
    C = parent_instance.total_annual_cost(Q, T_p)

    return {"T_p": T_p, "Q": Q, "C": C}

# def calculate_cost(parameters, buyer_num, item_num):
#     demand = []
#     purchasing_cost = []
#     time_multipliers = []
#     major_setup_cost = 0.0
#     variable_cost = []
#     minor_setup_cost = []

#     for i in range(buyer_num):
#         buyer_name = f'buyerName{i}'
#         major_setup_key = f'majorSetupCost{i}'
#         buyer_info = parameters.get(buyer_name, {})
#         if buyer_info:
#             major_setup_val = buyer_info.get(major_setup_key, 0.0)
#             if major_setup_val is not None:
#                 major_setup_cost += float(major_setup_val)

#         items_data = parameters.get(f'Items data{i}', [])
#         for item in items_data:
#             demand.append(item.get('demand'))
#             purchasing_cost.append(item.get('price'))
#             time_multipliers.append(item.get('frequency'))
#             variable_cost.append(item.get('inventoryCarryingCharge'))
#             minor_setup_cost.append(item.get('minorSetupCost', 0))
#             print(demand)
#             print(major_setup_cost)
#             print(purchasing_cost)
#             print(time_multipliers)
#             print(variable_cost)

#     if not all(isinstance(param, list) for param in [demand, purchasing_cost, time_multipliers, variable_cost]):
#         return {"error": "Parameters must be provided as lists"}
    

#     parent_instance = Parent(demand, buyer_num, item_num, purchasing_cost, time_multipliers, major_setup_cost, minor_setup_cost, variable_cost)

#     T_p, k_ijq = parent_instance.rand_algorithm(demand, time_multipliers)
#     Q = parent_instance.order_quantity(demand, T_p)
#     C = parent_instance.total_annual_cost(Q, T_p)

#     return {"T_p": T_p, "Q": Q, "C": C}





# Main function
# def main():
#     # Run Goyal algorithm
#     # mjrp.py

#     T_p, k_ijq = rand_algorithm(demand, k_ij)

#     # Use the optimal T_p and k_ijq to compute the optimal order quantity Q
#     Q = order_quantity(demand, T_p)

#     # Compute total relevant cost
#     C = total_annual_cost(Q, T_p)

#     print("Optimal cycle time T_p:", T_p)
#     print("Optimal order quantity Q:", Q)
#     print("Total relevant cost C:", C)

# # Execute main function
# if __name__ == "__main__":
#     main()
