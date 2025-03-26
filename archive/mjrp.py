# def random():
#     return "Hello"
# 
# var = random()
# print(var)

#j item number
# n buyer number
# d demand per unti time of item i in buyer j
# S the major set up cost
# s the minor set up cost when item i is included in a group replenishment in buyer j
# v the unit variable cost of item i
# r the inventory carrying charge in per unit time
# C the total relevant cost
# t the basic cycle time interval between orders, a decision variable;
# k the number of integer multiples of T that a replenishment of item i is included in a group replenishment in buyer j, a decision variable;
# Q the order quantity of item i for buyer j, a decision variable
import math

def cycle_time(k, t):
    T = k * t
    return T

def order_quantity(demand):
    T_q = cycle_time()
    Q = T_q * demand
    return Q

def holding_cost(item_num, buyer_num, Q, v, r):
    arr = []
    for i in buyer_num:
        for j in item_num:
            holding_cost = (Q[i][j] * v[i] * r)/2
            arr.append(holding_cost)
    return sum(arr)

def set_up_costs(S, s, k, buyer_num, item_num):
    T = cycle_time
    cons = S/T
    set_up_array = []
    for i in buyer_num:
        for j in item_num:
            set_up_cost = s[i][j]/(k[i][j] * T)
            set_up_array.append(set_up_cost)
    Total_set_up_cost = cons + sum(set_up_array)
    return Total_set_up_cost

def total_annual_cost():
    Total_holding_cost = holding_cost()
    Total_setup_cost = set_up_costs()
    return Total_holding_cost + Total_setup_cost

# RAND Algorithm
# helper functions
def func1(item_num, buyer,num, s, S):
    set_up_array = []
    for i in buyer_num:
        for j in item_num:
            set_up_array.append(s[i][j])
    return S + sum(set_up_array)
    
def func2(item_num, buyer,num, d, v, r):
    demand_array = []
    for i in buyer_num:
        for j in item_num:
            demand_array.append(s[i][j]*v[i])
    return r * sum(demand_array)

# functions to find tmax
def find_cycle_time_max():
    var_1 = func1()
    var_2 = func2()
    T_max = math.sqrt((2 * var_1)/var_2)
    return T_max

#functions to find Tmin
# helper functions for tmin
def t1_helper_function(s, r, d, v, buyer_num, item_num):
    t1_array = []
    for i in buyer_num:
        for j in item_num:
            t_variable = math.sqrt((2 * s) / (r * d * v))
            t1_array.append(t_variable)
            return min(t1_array)
            
def func_min1(s, k, buyer_num, item_num, S):
    t1 = t1_helper_functions()
    array1 = []
    for i in buyer_num:
        for j in item_num:
            set_up_cost = s[i][j]/(k[i][j] * t1)
            array1.append(set_up_cost)
    return S + sum(array1)

def func_min2(d, v, k, r, buyer_num, item_num):
    t1 = t1_helper_functions()
    array2 = []
    for i in buyer_num:
        for j in item_num:
            demand_cost = d[i][j] * v[i] / k[i][j] * t1
            array2.append(demand_cost)
    return r * sum(array2)

def find_cycle_time_min():
    var_1 = func_min1()
    var_2 = func_min2()
    Tmin = math.sqrt((2 * var_1)/ var_2)
    return Tmin

# main iteration
# def main():
#     t_max = find_cycle_time_max()
#     t_min = find_cycle_time_min()
    


    
            
    
    