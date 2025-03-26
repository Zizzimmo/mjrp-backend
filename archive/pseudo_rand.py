import math
import sys

# using taolu's data for both demands and minor setup costs
d = [[11, 24, 6, 19, 20, 4,19],[9, 56, 8, 25, 23, 10,50],[5,51,6,25,17,3,32],[2,6,1,5,5,2,8],[11,45,6,31,22,6,31],[8,46,9,31,27,3,28],[11,55,7,21,24,8,47]]
s = [[150, 100, 100, 50, 50, 50, 50], [100, 150, 100, 100, 50, 100, 150],[50,150,100,100,50,50,100],[50,50,50,50,50,50,100],[150,150,100,100,50,100,100],[100,150,100,100,50,100,150], [150,150,100,100,50,100,150]]
S = 8000
r = .3
v = [800, 400, 800, 400, 270, 900, 350]
k = [[4,4,3,4,7,7,5],[3,4,4,10,10,4,4],[3,4,3,3,4,10,4],[20,5,20,20,20,10,20,7],[3,4,3,3,3,20,3],[3,3,3,10,10,3,4],[7,6,7,2,2,6,5]]
buyer_num = 7
item_num = 7

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
# cycle time
    def cycle_time(self, T_, k):
        print(T_)
        arr = []
        for i in range(buyer_num):
            for j in range(item_num):
                arr.append(k[i][j] * T_)
        return arr

# function that reshapes an array from 1d to 2d
    def reshape_array(self, arr, rows, cols):
        if rows * cols != len(arr):
            raise ValueError("Number of elements in the array does not match the desired shape")

        reshaped_array = []
        for i in range(0, len(arr), cols):
            reshaped_array.append(arr[i:i+cols])

        return reshaped_array

# order quantity
    def order_quantity(T, d):
        Q = []
        print(len(T))
        print(T)
        print(d)
        T_new = reshape_array(T, 7, 7)
        print(T_new)
        for i in range(buyer_num):
            for j in range(item_num):
                Q.append(round((T_new[i][j] * d[i][j])))
        return Q

# Function for calculating total holding costs
    def total_holding_cost(self, Q, v, r):
        holding_cost = []
        cons = r/2
        print(Q)
        Q_new = reshape_array(Q, 7, 7)
        for i in range(buyer_num):
            for j in range(item_num):
                holding_cost.append( cons * Q_new[i][j] * v[j])
        holding_cost_sum = sum(holding_cost)
        return holding_cost_sum

# function for calculating total setup costs
    def total_setup_cost(self, s, S, k, T):
        set_up_cost = []
        cons = S/T
        for i in range(buyer_num):
            for j in range(item_num):
                set_up_cost.append( s[i][j] / (k[i][j] * T))
        res = cons + sum(set_up_cost)
        return res

# function for calculating the total annual costs i.e. total setup cost + total holding cost = total annual cost
    def total_annual_cost(self,Q, v, r, s, S, k, T):
        var1 = total_holding_cost(Q, v, r)
        var2 = total_setup_cost(s, S, k, T)
        return var1 + var2

    # helper functions to determine the values of Tmin and Tmax
    # helper functions for finding T_max
    def t_max_helper_function1(self, S, s):
        array = []
        for i in range(buyer_num):
            for j in range(item_num):
                array.append(s[i][j])
        res = 2 * (S + sum(array))
        return res

    def t_max_helper_function2(r, d, v):
        array = []
        for i in range(buyer_num):
            for j in range(item_num):
                array.append( d[i][j] * v[j] )
        res = r * sum(array)
        return res

# main function that calculates tmax
    def find_tmax(S, s, r, d, v):
        var1 = t_max_helper_function1(S, s)
        var2 = t_max_helper_function2(r, d, v)
        return math.sqrt(var1 / var2)

    # function to find t1
    def t1_finder(s, r, d, v):
        array = []
        for i in range(buyer_num):
            for j in range(item_num):
                array.append(math.sqrt(( 2 * s[i][j] )/ ( r * d[i][j] * v[j] )))
        return min(array)

    def t_min_helper_function1(S, s, k, t1):
        array = []
        for i in range(buyer_num):
            for j in range(item_num):
                array.append( s[i][j] / ( k[i][j] * t1) )
        res = 2 * ( S + sum(array) )
        return res

    def t_min_helper_function2(r, d, v, k, t1):
        array = []
        for i in range(buyer_num):
            for j in range(item_num):
                array.append( (d[i][j] * v[j]) / ( k[i][j] * t1 ))
        res = r * sum(array)
        return res

    # main function to find tmin
    def find_tmin(S, s, k, r, d, v):
        t1 = t1_finder(s, r, d, v)
        var1 = t_min_helper_function1(S, s, k, t1)
        var2 = t_min_helper_function2(r, d, v, k, t1)
        return math.sqrt(var1/var2)

    # function for finding step 2, the decision maker
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
        print (cycle_times)

        return cycle_times

    # function to compute k_ijq
    def compute_k_ijq(self, cycle_times, d):  # Renamed parameter to clarify
        k_ijq = []
        for cycle_time in cycle_times:  # Iterate through the list of cycle times
            inner_k_row = []
            for i in range(buyer_num):
                k_row = []
                for j in range(item_num):
                    if d[i][j] == 0:
                        k_row.append(float('inf'))
                    else:
                        k_row.append((2 * s[i][j] * cycle_time**2) / math.sqrt(r * d[i][j] * v[j]))
                        inner_k_row.append(k_row)  # Append the k_row for each cycle time
            k_ijq.append(inner_k_row) # Append the inner list for all cycle times
        print(k_ijq)
        return k_ijq


    # threshold checker to calculate and find k_star
    def compute_k_star(k):
        k_star = []
        upper_limit = l*(l+1)
        lower_limit = l(l-1)
        for i in range(len(k)):
            if k[i]**2 > lower_limit and k[i]**2 < lower_limit:
                k_star.append(l)
            else:
                k_star.append(math.sqrt(k[i]))
        return k_star

    # computes a new cycle time Tp
    def new_cycle_time(S, s, k_star, r, d, v):
        var1 = numerator(S, s, k_star)
        var2 = denominator(r, d, v, k_star)
        return math.sqrt(var1/var2)

    def find_kp(kijq, L):
        kp = []
        upper_limit = L * (L+1)
        lower_limit = L * (L-1)
        for z in range(len(kijq)):
            print(len(kijq[z]))
            for i in range(buyer_num):
                print(len(kijq[z][i]))
                kp_row = []
                for j in range(item_num):
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
    def numerator(S, s, k_star):
        arr = []
        print(s)
        for i in range(len(s)):
            for j in range(item_num):
                if k_star[i][j] == 0:  # Check for division by zero
                    arr.append(float('inf'))  # Append infinity for division by zero
                else:
                    arr.append(s[i][j] / k_star[i][j])
        res = 2 * ( S + sum(arr))
        return res

    def denominator( r, d, v, k_star):
        arr = []
        for i in range(buyer_num):
            for j in range(item_num):
                arr.append(d[i][j] * v[j] * k_star[i][j])
        res = r * sum(arr)
        return res



    # the main RAND algorithm
    def rand(demand, k):
        # step 1: determine Tmin and Tmax
        t_max = find_tmax(S, s, r, d, v)
        t_min = find_tmin(S, s, k ,r ,d ,v)
        print(t_min)
        print(t_max)
        
        min_C = float('inf')
        best_solution = None
        
        l = 5
        cycle_times = decision_maker(t_max, t_min)
        print(cycle_times)
        # step 3: set p = p + 1, q = 0
        p = 0
        k_ijq = compute_k_ijq(cycle_times, d)
        k_star = find_kp(k_ijq, l)
        print("K_star is = ",k_star)
        print(type(s))
        new_tp = new_cycle_time(S, s, k_star, r , d, v)
        print("new Tp value: ", new_tp)
                
                # step 4: set q = q + 1
                # compute k**2 for T_p
                # returns the squared value of k_ijq
        
                # step 5: for each (i, j) find k*ijq 
    #     if new_tp == cycle_time:
    #         pass
    #     else:
    #         cycle_time = new_cycle_time
            
    #     C = total_annual_cost(Q, t_p)
    #     if C < min_C:
    #         min_C = C
        best_solution = (new_tp, k_star)
                
        return best_solution
        
            
    # def main():
    #     T_p, k_ijq = rand(d, k)
    #     print(T_p)
    #     T_y = cycle_time(T_p, k_ijq)
    # #     print(T_y)
    #     Q = order_quantity(T_y, d)
    #     C = total_annual_cost(Q, v, r, s, S, k_ijq, T_p)
        
    #     print("Optimal cycle time T_p:", T_p)
    #     print("Optimal order quantity Q:", Q)
    #     print("length of optimal quantity array:", len(Q))
    #     print("Total relevant cost C:", C)
    
        

    
    

    



