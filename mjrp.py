import math
import sys

# using taolu's data for both demands and minor setup costs
# d = [[11, 24, 6, 19, 20, 4,19],[9, 56, 8, 25, 23, 10,50],[5,51,6,25,17,3,32],[2,6,1,5,5,2,8],[11,45,6,31,22,6,31],[8,46,9,31,27,3,28],[11,55,7,21,24,8,47]]
# s = [[150, 100, 100, 50, 50, 50, 50], [100, 150, 100, 100, 50, 100, 150],[50,150,100,100,50,50,100],[50,50,50,50,50,50,100],[150,150,100,100,50,100,100],[100,150,100,100,50,100,150], [150,150,100,100,50,100,150]]
# major_setup_cost = 8000
# r = .3
# v = [800, 400, 800, 400, 270, 900, 350]
# k = [[4,4,3,4,7,7,5],[3,4,4,10,10,4,4],[3,4,3,3,4,10,4],[20,5,20,20,20,10,20,7],[3,4,3,3,3,20,3],[3,3,3,10,10,3,4],[7,6,7,2,2,6,5]]
# buyer_num = 7
# item_num = 7

class Parent:
    def __init__(self,  demand, purchasing_cost, time_multipliers, minor_setup_cost, buyer_num, item_num, major_setup_cost, inventory_carrying_charge):
        self.d = demand
        self.major_setup_cost = major_setup_cost
        self.s = minor_setup_cost
        self.r = inventory_carrying_charge
        self.v = purchasing_cost
        self.k = time_multipliers
        self.buyer_num = buyer_num
        self.item_num = item_num

# cycle time
    def cycle_time(self, T_, k):
        print(T_)
        arr = []
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                arr.append(k[i][j] * T_)
        return arr

# function that reshapes an array from 1d to 2d
    def reshape_array(self, arr, rows, cols):
#         print(rows)
#         print(cols)
#         print(len(arr))
        if rows * cols != len(arr):
            raise ValueError("Number of elements in the array does not match the desired shape")

        reshaped_array = []
        for i in range(0, len(arr), cols):
            reshaped_array.append(arr[i:i+cols])

        return reshaped_array

# order quantity
    def order_quantity(self, T, d):
        Q = []
#       print(len(T))
#         print(T)
    # print(d)
        T_new = self.reshape_array(T, self.buyer_num, self.item_num)
        print(T_new)
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                Q.append(round((T_new[i][j] * d[i][j])))
        return Q

# Function for calculating total holding costs
    def total_holding_cost(self, Q, v, r):
        holding_cost = []
        cons = r/2
        # print(Q)
        Q_new = self.reshape_array(Q, self.buyer_num, self.item_num)
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                holding_cost.append( cons * Q_new[i][j] * v[j])
        holding_cost_sum = sum(holding_cost)
        return holding_cost_sum

# function for calculating total setup costs
    def total_setup_cost(self, s, major_setup_cost, k, T):
        set_up_cost = []
        cons = major_setup_cost/T
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                set_up_cost.append( s[i][j] / (k[i][j] * T))
        res = cons + sum(set_up_cost)
        return res

# function for calculating the total annual costs i.e. total setup cost + total holding cost = total annual cost
    def total_annual_cost(self, Q, v, r, s, major_setup_cost, k, T):
        var1 = self.total_holding_cost(Q, v, r)
        var2 = self.total_setup_cost(s, major_setup_cost, k, T)
        return var1 + var2

# helper functions to determine the values of Tmin and Tmax
# helper functions for finding T_max
    def t_max_helper_function1(self, major_setup_cost, s):
        array = []
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                array.append(s[i][j])
        res = 2 * (major_setup_cost + sum(array))
        return res

    def t_max_helper_function2(self, r, d, v):
        array = []
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                array.append( self.d[i][j] * self.v[j])
        res = r * sum(array)
        return res

# main function that calculates tmax
    def find_tmax(self, major_setup_cost, s, r, d, v):
        var1 = self.t_max_helper_function1(major_setup_cost, s)
        var2 = self.t_max_helper_function2(r, d, v)
        return math.sqrt(var1 / var2)

# function to find t1
    def t1_finder(self, s, r, d, v):
        array = []
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                array.append(math.sqrt(( 2 * s[i][j] )/ ( r * d[i][j] * v[j] )))
        return min(array)

    def t_min_helper_function1(self, major_setup_cost, s, k, t1):
        array = []
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                array.append( s[i][j] / ( k[i][j] * t1) )
        res = 2 * ( major_setup_cost + sum(array) )
        return res

    def t_min_helper_function2(self, r, d, v, k, t1):
        array = []
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                array.append( (d[i][j] * v[j]) / ( k[i][j] * t1 ))
        res = r * sum(array)
        return res

# main function to find tmin
    def find_tmin(self, major_setup_cost, s, k, r, d, v):
        t1 = self.t1_finder(s, r, d, v)
        var1 = self.t_min_helper_function1(major_setup_cost, s, k, t1)
        var2 = self.t_min_helper_function2(r, d, v, k, t1)
        return math.sqrt(var1/var2)

# function for finding step 2, the decision maker
    def decision_maker(self, T_min, T_max):
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
        print (cycle_times)

        return cycle_times

    # function to compute k_ijq
    def compute_k_ijq(self, cycle_times, d):  # Renamed parameter to clarify
        k_ijq = []
        for cycle_time in cycle_times:  # Iterate through the list of cycle times
            inner_k_row = []
            for i in range(self.buyer_num):
                k_row = []
                for j in range(self.item_num):
                    if d[i][j] == 0:
                        k_row.append(float('inf'))
                    else:
                        k_row.append((2 * self.s[i][j] * cycle_time**2) / math.sqrt(self.r * d[i][j] * self.v[j]))
                        inner_k_row.append(k_row)  # Append the k_row for each cycle time
            k_ijq.append(inner_k_row) # Append the inner list for all cycle times
        print(k_ijq)
        return k_ijq


# threshold checker to calculate and find k_star
    def compute_k_star(self, k):
        k_star = []
        l = 5
        upper_limit = l*(l+1)
        lower_limit = l(l-1)
        for i in range(len(k)):
            if k[i]**2 > lower_limit and k[i]**2 < lower_limit:
                k_star.append(l)
            else:
                k_star.append(math.sqrt(k[i]))
        return k_star

# computes a new cycle time Tp
    def new_cycle_time(self, major_setup_cost, s, k_star, r, d, v):
        var1 = self.numerator(major_setup_cost, s, k_star)
        var2 = self.denominator(r, d, v, k_star)
        return math.sqrt(var1/var2)

    def find_kp(self, kijq, L):
        kp = []
        upper_limit = L * (L+1)
        lower_limit = L * (L-1)
        for z in range(len(kijq)):
            # print(len(kijq[z]))
            for i in range(self.buyer_num):
                print(len(kijq[z][i]))
                kp_row = []
                for j in range(self.item_num):
                    value = kijq[z][i][j]
                    if lower_limit < value < upper_limit:
                        kijq[z][i][j] = L
                        kp_row.append(value)
                    else:
                        kijq[z][i][j] = math.sqrt(value)
                        kp_row.append(value)
                kp.append(kp_row)
                    
        return kp

# helper function for finding new cycle time using the generated k_star
    def numerator(self, major_setup_cost, s, k_star):
        arr = []
#         print(s)
        for i in range(len(s)):
            for j in range(self.item_num):
                if k_star[i][j] == 0:  # Check for division by zero
                    arr.append(float('inf'))  # Append infinity for division by zero
                else:
                    arr.append(s[i][j] / k_star[i][j])
        res = 2 * ( major_setup_cost + sum(arr))
        return res

    def denominator( self, r, d, v, k_star):
        arr = []
        for i in range(self.buyer_num):
            for j in range(self.item_num):
                arr.append(d[i][j] * v[j] * k_star[i][j])
        res = r * sum(arr)
        return res

# the main RAND algorithm
    def rand(self, d, k):
        # step 1: determine Tmin and Tmax
        t_max = self.find_tmax(self.major_setup_cost, self.s, self.r, d, self.v)
        t_min = self.find_tmin(self.major_setup_cost, self.s, k , self.r , d , self.v)
        print(t_min)
        print(t_max)
        
        min_C = float('inf')
        best_solution = None
        
        l = 5
        cycle_times = self.decision_maker(t_max, t_min)
#         print(cycle_times)
        # step 3: set p = p + 1, q = 0
        p = 0
        k_ijq = self.compute_k_ijq(cycle_times, d)
        k_star = self.find_kp(k_ijq, l)
#         print("K_star is = ",k_star)
#         print(type(s))
        new_tp = self.new_cycle_time(self.major_setup_cost, self.s, k_star, self.r , d, self.v)
        print("new Tp value: ", new_tp)
        best_solution = (new_tp, k_star)
                
        return best_solution

    def get_array_lengths(self, data):
            buyer_num = len(data)
            try:
                item_num = len(data[0]['itemsData']) if data else 0
            except Exception as e:
                print("Error:", e)
                print("Data:", data)
                item_num = 0
            return buyer_num, item_num


def calculate_cost(parameters,  buyer_num, item_num, major_setup_cost, inventory_carrying_charge ):
    print("parameters:", parameters)
    demand = parameters.get('demand', [])
    purchasing_cost_array = parameters.get('price', [])
    time_multipliers = parameters.get('frequency', [])
    minor_setup_cost = parameters.get('minorSetupCost', [])

    purchasing_cost = purchasing_cost_array[0]
    print("demand:", demand)
    print("price:", purchasing_cost )
    print("time_multipliers:", time_multipliers )
    print("minor_setup_cost:",  minor_setup_cost )

    # Check if all required parameters are extracted and of the correct type
    if demand is None or purchasing_cost is None or time_multipliers is None or major_setup_cost is None:
        return {"error": "Required parameters not provided"}

    # Ensure that the parameters are of the expected type (e.g., list)
    if not isinstance(demand, list) or not isinstance(purchasing_cost, list) \
            or not isinstance(time_multipliers, list):
        return {"error": "Parameters must be provided as lists"}
    
    parent_instance = Parent(demand, purchasing_cost, time_multipliers, minor_setup_cost, buyer_num, item_num, major_setup_cost, inventory_carrying_charge)

    T_p, k_ijq = parent_instance.rand(demand, time_multipliers)
    T_y = parent_instance.cycle_time(T_p, k_ijq)
    Q = parent_instance.order_quantity(T_y, demand)
    C = parent_instance.total_annual_cost(Q, purchasing_cost, inventory_carrying_charge, minor_setup_cost, major_setup_cost, k_ijq, T_p)

    return {"T_p": T_p, "Q": Q, "C": C}