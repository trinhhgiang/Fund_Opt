import time
import sys
from read_data import*
# return the sublist of a list
def sublist(lst):
    if lst == []:
        return [[]]
    else:
        x = sublist(lst[1:])
        return x + [[lst[0]] + y for y in x]

# eliminate unqualified list
def candidate(k):
    lst = sublist(avai_farm[k])
    # constraint of m and M
    for i in lst[1:]:
        _d= 0
        for j in i:
            _d += d[j - 1]    
        if _d < m or _d > M:
            lst.remove(i)        
    return lst

# backtracking
def solve(k):
    for i in candidate(k):
        sol[k] = i
        if k == n-1 :
            lst_sol.append(sol[:])
        else:
            solve(k+1)

# final elimination    
def result():
    # check for farms occuring 2 or more.
    for i in lst_sol[:]:
        test = []
        for j in i:
            test += j 
        for l in test[:]:
            if test.count(l) > 1:
                lst_sol.remove(i)
                break  
    # check for whether there are enough farms.  
    for i in lst_sol[:]:
        s = 0
        for j in i:
            s += len(j)
        if s != N:
            lst_sol.remove(i) 
    # calculate the final result.
    lst_opt_sol = []
    lst_val = []
    opt_val = M
    for i in lst_sol:
        maxsum = 0
        minsum = M
        for j in i:
            sum_ = sum(list(map(lambda x: d[x-1], j)))
            if sum_ == 0:
                continue
            if  sum_ > maxsum:
                maxsum = sum_
            if sum_ < minsum:
                minsum = sum_
        value = maxsum - minsum
        if value <= opt_val:
            if value == opt_val:
                lst_opt_sol.append(i)
            else:
                opt_val = value
                lst_opt_sol = []
                lst_opt_sol.append(i)
        lst_val.append(value)
    return (lst_sol, lst_val, lst_opt_sol, opt_val)

def convert_data(s, e, n, N):
    avai_farm = [[] for _ in range(n)]
    for i in range(N):
        for j in range(s[i]-1, e[i]):
            avai_farm[j].append(i)
    return avai_farm

def main():
    global n, N, m, M, avai_farm, d, sol, lst_sol
    data=sys.argv[1]
    N, m, M, d, s, e, n=read_input_file(data)
    # available farm in each day
    # avai_farm = [[3, 4, 5, 8],
    #             [1, 3, 4, 5, 7, 8],
    #             [1, 2, 3, 4, 5, 7],
    #             [1, 2, 4, 6, 7],
    #             [4, 6, 7]]

    # avai_farm = [[2, 3],
    #             [1, 2, 3, 6],
    #             [1, 3, 4, 6, 8],
    #             [1, 4, 5, 7, 8],
    #             [5, 7, 8]]
    # s = [2, 1, 1, 3, 4, 2, 4, 3]
    # e = [4, 2, 3, 4, 5, 3, 5, 5]
    # n = 5
    # N = 8
    avai_farm = convert_data(s, e, n, N)
    # # production of each farm
    # production = [6, 8, 3, 1, 5, 7, 2, 4]
    # # production = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # m = 10
    # M = 14

    # m = 30
    # M = 100
    # production = [8,9,12,15,20,17,19,6,7,22,16,15,17,5,9,15,20,25,10,18]
    # # s = [2,5,3,1,4,4,5,2,4,3,2,3,2,1,4,5,4,1,2,3]
    # # e = [5,9,7,8,6,8,8,7,6,6,6,6,5,7,8,10,8,8,7,6]
    # avai_farm = [[4, 14, 18],
    # [1, 4, 8, 11, 13, 14, 14, 18, 19],
    # [1, 3, 4, 8, 10, 11, 12, 13, 14, 18, 19, 20],
    # [1, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20],
    # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 , 13, 14, 15, 16, 17, 18, 19, 20],
    # [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20],
    # [2, 3, 4, 6, 7, 8, 14, 15, 16, 17, 18, 19],
    # [2, 4, 6, 7, 15, 16, 17, 18],
    # [2, 16],
    # [16]]
    # N = len(production)
    # n = len(avai_farm)
    sol = [0]*n
    lst_sol = []

    solve(0)
    print('All solutions:')
    print(result()[0])
    print('All values:')
    print(result()[1])
    print('Optimal solutions:')
    print(result()[2])
    print('Optimal value:')
    print(result()[3])

start_time = time.time()
main()
end_time = time.time()
print('Time: ', end_time - start_time)


