import math
import random


# Define parameters
item_num = 7
buyer_num = 7



# Given parameters
S = 8000	# Major setup cost
demand = [[11,24,6,19,20,4,19],[9,56,8,25,23,10,50],[5,51,6,25,17,3,32],[2,6,1,5,5,2,8],[11,45,6,31,22,6,31],[8,46,9,31,22,6,31],[11,55,7,21,24,8,47]]  #demand per unit time
v = [800,400,800,400,270,900,350]  # Unit price
r = 0.3  # Inventory carrying charge per unit time
s = [[150,100,100,50,50,50,50],[100,150,100,100,50,100,150],[50,150,100,100,50,50,100],[50,50,50,50,50,50,100],[150,150,100,100,50,100,100],[100,150,100,100,100,50,100],[150,150,100,100,100,50,100]] #minor setup cost	
k_ij = [[6,6,8,5,3,3,4],[8,6,6,2,2,5,6],[7,6,7,7,5,2,5],[1,4,1,1,2,1,3],[7,6,7,4,5,7,6],[8,5,8,6,7,1,3],[7,6,7,2,2,6,5]] 
B = 20000 # Budget limitation
lagrange_multiplier_value = None

# Function to compute cycle time
def cycle_time(k, t):
    T = k * t
    return T

# Function to compute order quantity
def order_quantity(demand, T):
    Q = []
    for i in range(buyer_num):
        buyer_demand = []
        for j in range(item_num):
            buyer_demand.append(T * demand[i][j])
        Q.append(buyer_demand)
    return Q

        
def item_holding_cost(r, v): # the algorithm representation of r * v
    item_holding_cost_array = []
    for i in range(len(v)):
        item_holding_cost_array.append(r * v[i])
    return item_holding_cost_array
 
# Function to compute holding cost
def holding_cost(Q, v, r):
    total_holding_cost = 0
    for i in range(buyer_num):
        for j in range(item_num):
            total_holding_cost += (Q[i][j] * v[j] * r) / 2
    return total_holding_cost

# Function to compute setup costs
def set_up_costs(k, T):
    cons = S / T
    set_up_array = []
    for i in range(buyer_num):
        for j in range(item_num):
            if k[i][j] == 0:
                set_up_cost = float('inf')
                set_up_array.append(set_up_cost)
            else:    
                set_up_cost = s[i][j] / (k[i][j] * T)
                set_up_array.append(set_up_cost)
    total_set_up_cost = cons + sum(value for value in set_up_array if value != float('inf'))
    return total_set_up_cost

# Function to compute total annual cost
def total_annual_cost(Q, T):
    total_holding_cost = holding_cost(Q, v, r)
    total_setup_cost = set_up_costs(Q, T)
    return total_holding_cost + total_setup_cost

def decision_maker(T_min, T_max):
    """
  Divides the range [T_min, T_max] into l-1 equally spaced intervals of cycle time T.

  Args:
      T_min: Minimum cycle time.
      T_max: Maximum cycle time.
      l: Number of intervals (including T_min and T_max).

  Returns:
      A list of cycle times (T1, T2, ..., Tl) representing the divided intervals.
  """
    l = 5
    if l <= 1:
        raise ValueError("Number of intervals (l) must be greater than 1.")
    

  # Calculate the interval size (T)
    T = (T_max - T_min) / (l - 1)

  # Create a list of cycle times within the intervals
    cycle_times = [T_min + i * T for i in range(l)]

    return cycle_times

def threshold_checker(k, l):
    upper_limit = l*(l+1)
    lower_limit = l(l-1)
    for i in range(len(k)):
        if k[i]**2 > lower_limit and k[i]**2 < lower_limit:
            k[i] = l
    return k

def budget_checker(Q, B):
  meet_budget_criterion = []
  z_array = []
  for i in range(buyer_num):  # Loop through buyers
    budget_array = []
    for j in range(item_num):  # Loop through items for each buyer
      budget_array.append((Q[i][j] * v[j]))  # Calculate cost for each item-buyer pair
    z_array.append([0 if value <= B else 1 for value in budget_array])  # Check budget for each item
  return z_array

#lagrange multiplier
def lagrange_multiplier(k_ij, T_p):
    print(k_ij)
    var1 = lagrange_helper_function1(S, s, k_ij, T_p)
    var2 = lagrange_helper_function2(d, k_ij)
    var3 = lagrange_helper_function3(d, v, k_ij)
    if var3 != 0:
        expr = (var1 - var2)/var3
    else:
        expr = 0
    return expr

def lagrange_helper_function1(S, s, k, T_p):
    for i in range(buyer_num):
        array = []
        for j in range(item_num):
            if k[i][j] == 0:
                array.append(float('inf'))
            else:
                array.append(s[i][j]/k[i][j])
    return (S + sum(value for value in array if value != float('inf')))/T_p**2

def lagrange_helper_function2(d, k, q):
    h = item_holding_cost(v, r)
    for i in range(buyer_num):
        array = []
        for j in range(item_num):
            array.append((d[i][j] * h[i][j] * k)/2)
    return sum(array)

def lagrange_helper_function3(d, v, k):
    array = []
    for i in range(buyer_num):
        for j in range(item_num):
            array.append((d[i][j] * v[j] * k[i][j]))
    return sum(array)

def z_checker(z):
    if z == 0:
        lagrange_multiplier_value = 0
    else:
        lagrange_multiplier_value = lagrange_multiplier()
    return lagrange_multiplier_value

# calculates new k- based on lagrange value, holding cost, price, and T_p**2
def k_q_calculator(s,demand, v, T_p):
    lang = lagrange_multiplier(k_ij)
    h = item_holding_cost(r, v)
    k_ijq_array = []
    for i in range(buyer_num):
        for j in range(item_num):
            k_ijq_array.append((2 * s[i][j] )/ ((demand[i][j] * h[j]) + 2 * lang * demand[i][j] * v[j]) * (T_p ** 2)) 
    return k_ijq_array

def minimum_period(S, s, k, demand, v, B):
    var_1 = minimum_period_helper_function1
    var_2 = minimum_period_helper_function2
    var_3 = minimum_period_helper_function3
    
    T_p = min(math.sqrt(var_1/var_2),var_3)
    
def minimum_period_helper_function1(S, s, k):
    array1 = []
    for i in buyer_num:
        for j in item_num:
            if k[i][j] == 0:
                array1.append(float('inf'))
            else:
                array1.append((s[i][j] / k[i][j]))
    return 2*(S + sum(value for value in array1 if value != float('inf')))

def minimum_period_helper_function2(demand, k):
    h = item_holding_cost(r, v)
    array2 = []
    for i in buyer_num:
        for j in item_num:
            if k[i][j] == 0:
                array2.append(float('inf'))
            else:
                array2.append((d[i][j] * h[j])/k[i][j])
    return sum(value for value in array2 if value != float('inf'))    

def minimum_period_helper_function3(demand, B, k, v):
    denominator = []
    for i in buyer_num:
        for j in item_num:
            denominator.append((demand[i][j] * v[j] * k[i][j]))
    denominator_sum = sum(denominator)
    return B / denominator_sum
       
# Rand Algorithm
def rand_algorithm(demand, k_ij):
    # Step 1: Initialize parameters
    t_max = find_cycle_time_max()
    t_min = find_cycle_time_min()
    print(t_min)
    print(t_max)
    
    
    cycle_times = decision_maker(t_max, t_min)
    print("interval length:", len(cycle_times))

    # Step 2: Initialize variables
    p = 0
    for T_p in cycle_times:
        # Start with the minimum cycle time
        k_q = []
        lagrange_array = []
        p, z, q = p + 1, 0, 0
        q = q + 1
        
        # Initialize iteration counter
        k_ijq = compute_k_ijq(T_p, demand)
        T_p = compute_new_cycle_time(k_ijq)
        k_q.append(k_ijq)
        lagrange_multiplier(k_ijq, T_p)
        
        array = k_q_calculator(s, demand, v, T_p)
                
        # Step 7: Check for convergence
        if q == 1 or not_condition_met(k_ijq):
            q += 1
        else:
            converged = True

    return T_p, k_ijq

# Function to compute k_ijq
def compute_k_ijq(T_p, demand):
    k_ijq = []
    for i in range(buyer_num):
        for j in range(item_num):
            if demand[i][j] == 0:
                k_ijq.append(float('inf'))
            else:
                k_ijq.append(2 * s[i][j] * T_p**2 / math.sqrt(r * demand[i][j] * v[j]))
    return k_ijq

# Function to compute new cycle time T_p
def compute_new_cycle_time(k_ijq):
    numerator = 2 * S
    denominator = sum(value for value in k_ijq if value != float('inf'))
    if denominator == 0:
        T_p = float('inf')
    else:
        T_p = math.sqrt(numerator / denominator)
    return T_p

# Function to check condition for Step 7
def not_condition_met(k_ijq):
    # Check if kp_ijq - kp_ijq-1 = 1 for any i and j
    # If condition is met, return True; otherwise, return False
    # Implementation depends on specific condition in your problem
    return False

# Helper functions and functions for finding t_max and t_min (to be implemented)
def func1(item_num, buyer_num, s, S):
    set_up_array = []
    for i in range(buyer_num):
        for j in range(item_num):
            set_up_array.append(s[i][j])
    return S + sum(set_up_array)
    
def func2(item_num, buyer_num, d, v, r):
  demand_array = []
  print(len(d))
  print(item_num)
  print(len(v))
  for i in range(len(d)):  # Iterate up to the length of the list d
    print(i)
    for j in range(item_num):
        print(j)
        demand_array.append(d[i][j]*v[j])
  return r * sum(demand_array)

# functions to find tmax
def find_cycle_time_max():
    var_1 = func1(item_num, buyer_num, s, S)
    var_2 = func2(item_num, buyer_num, demand, v, r)
    print(var_1)
    print(var_2)
    T_max = math.sqrt((2 * var_1)/var_2)
    return round(T_max)

#functions to find Tmin
# helper functions for tmin
def t1_helper_function(s, r, d, v, buyer_num, item_num):
    t1_array = []
    for i in range(buyer_num):
        for j in range(item_num):
            if d[i][j] == 0:
                t_variable = float('inf')
                t1_array.append(t_variable)
            else:
                t_variable = math.sqrt((2 * s[i][j]) / (r[j] * d[i][j] * v[j]))
                t1_array.append(t_variable)
            return min(t1_array)

# code for finding the minimum cycle time
def find_t1(s, r, demand, v):
    t1_min = []
    
    # iteration over all elements of the demand matrix
    for i in range(buyer_num):
        for j in range(item_num):
            if demand[i][j] == 0:
                # Set expr to a large value (e.g., float('inf')) or skip the calculation
                expr = float('inf')
                t1_min.append(expr)
            else:
                expr = math.sqrt((2 * s[i][j]) / (r * demand[i][j] * v[j]))
                t1_min.append(expr)
    return min(t1_min)
            
def func_min1(s, k, buyer_num, item_num, S, t1):
    array1 = []
    for i in range(buyer_num):
        for j in range(item_num):
            if k[i][j] == 0:
                set_up_cost = float('inf')
                array1.append(set_up_cost)
            else:    
                set_up_cost = s[i][j]/(k[i][j] * t1)
                array1.append(set_up_cost)
    return S + sum(cost for cost in array1 if cost != float('inf'))

def func_min2(d, v, k, r, buyer_num, item_num, t1):
  array2 = []
  for i in range(buyer_num):
    for j in range(item_num):
        if k[i][j] != 0:  # Check if k is not zero (avoid division by zero)
            demand_cost = d[i][j] * v[j] / k[i][j] * t1
            array2.append(demand_cost)
        else:
            demand_cost = float('inf')
            array2.append(demand_cost)
    # Use list comprehension to filter out 'inf' values and sum the remaining elements
  return r * sum(cost for cost in array2 if cost != float('inf'))

def find_cycle_time_min():
    t1 = find_t1(s, r, demand, v)
    var_1 = func_min1(s, k_ij, buyer_num, item_num, S, t1)
    var_2 = func_min2(demand, v, k_ij, r, buyer_num, item_num, t1)
    print(var_1)
    print(var_2)
    Tmin = math.sqrt((2 * var_1)/ var_2)
    return round(Tmin)



    
# Main function
def main():
    # Run Goyal algorithm
    print(len(demand))
    print(len(s))
    print(len(v))
    print(len(k_ij))
    for i in range(len(demand)):
        print (len(demand[i]))
    T_p, k_ijq = rand_algorithm(demand, k_ij)

    # Use the optimal T_p and k_ijq to compute the optimal order quantity Q
    Q = order_quantity(demand, T_p)
    z_array = budget_checker(Q, B)
    res = None
    lagrange_array = []
    for i in z_array:
            res = z_checker(i)
            lagrange_array.append(res)

    # Compute total relevant cost
    C = total_annual_cost(Q, T_p)

    print("Optimal cycle time T_p:", T_p)
    print("Optimal order quantity Q:", Q)
    print("Total relevant cost C:", C)

# Execute main function
if __name__ == "__main__":
    main()
