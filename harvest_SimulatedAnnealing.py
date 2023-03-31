import random
import copy
import math 
import time
import sys
from read_data import*

data=sys.argv[1]
N, m, M, d, s, e, n=read_input_file(data)
# N = 20
# n = 10
# m = 30
# M = 100
# d=[8,9,12,15,20,17,19,6,7,22,16,15,17,5,9,15,20,25,10,18]
# s=[2,5,3,1,4,4,5,2,4,3,2,3,2,1,4,5,4,1,2,3]
# e=[5,9,7,8,6,8,8,7,6,6,6,6,5,7,8,10,8,8,7,6]

# N = 8
# n = 5
# m = 10
# M = 14
# d = [6, 8, 3, 1, 5, 7, 2, 4]
# s = [2, 1, 1, 3, 4, 2, 4, 3]
# e = [4, 2, 3, 4, 5, 3, 5, 5]

def random_harvest(s, e):
    lst = []
    for i in range(N):
        lst.append(random.randrange(s[i], e[i]+1))
    return lst

def day_plan(lst):
    idx = 1
    plan = [[] for _ in range(n)]
    for i in lst:
        plan[i-1].append(idx)
        idx += 1
    return plan

def loss_func(plan):
    loss = 0
    for i in plan:
        _sum = 0
        for j in i:
            _sum += d[j-1]
        if _sum == 0:
            continue
        loss += max(m - _sum, 0) + max(_sum - M ,0)
    return loss  

def feasible(plan, current_loss):
    neighbor = copy.deepcopy(plan)
    updated_loss = current_loss
    while updated_loss >= current_loss:
        neighbor = generate_neighbor(neighbor)
        updated_loss = loss_func(neighbor)
    return neighbor, updated_loss

def generate_neighbor(neighbor):
    move_field = random.randrange(1, N+1)
    day_move = random.randrange(s[move_field-1], e[move_field-1]+1)
    for i in range(n):
        if move_field in neighbor[i]:
            neighbor[i].remove(move_field)
            neighbor[day_move-1].append(move_field)
            break
    return neighbor

def optimization_score(sol):
    min_sum = M
    max_sum = 0
    for i in sol:
        _sum = 0
        for j in i:
            _sum += d[j-1]
        if _sum == 0:
            continue
        if _sum > max_sum:
            max_sum = _sum
        if _sum < min_sum:
            min_sum = _sum
    return max_sum - min_sum

def optimizing(plan, current_score):
    neighbor = copy.deepcopy(plan)
    opt_lst = []
    for _ in range(20):
        neighbor = generate_neighbor(neighbor)
        new_score = optimization_score(neighbor)
        if loss_func(neighbor) == 0:
            # print('hey', neighbor) 
            if new_score < current_score:
                # print('yes:', score)
                # print(neighborhood)
                opt_lst.append(copy.deepcopy(neighbor))
                current_score = new_score
            else:
                if random.random() < math.exp(-abs(new_score-current_score)):
                    # print('ok:', score)
                    # print(neighborhood)
                    current_score = new_score
            # neighborhood = copy.deepcopy(sol)
        else:
            neighbor = copy.deepcopy(plan)
            # print('here', neighbor)
    if len(opt_lst) == 0:
        opt_lst.append(plan)
    return opt_lst, current_score

def solve():
    print('5 feasible solutions:')
    final_sol_lst = []
    final_val_lst = []
    feasible_lst = []
    score_lst = []
    for _ in range(5):
        lst = random_harvest(s, e)
        sol = day_plan(lst)
        loss = loss_func(sol)
        for _ in range(20):
            if loss == 0:
                feasible_lst.append(sol)
                score = optimization_score(sol)
                score_lst.append(score)
                print(sol, loss)
                break
            sol, loss = feasible(sol, loss)
    print('Score:')
    print(score_lst)
    print()
    for i in range(5):
        final_sol, final_val = optimizing(feasible_lst[i], score_lst[i])
        final_sol_lst.append(final_sol)
        final_val_lst.append(final_val)
        # print(optimizing(feasible_lst[i], score_lst[i]))
    result = min(final_val_lst)
    print('Optimal result:', result)
    print('Solution:')
    for i in range(5):
        if final_val_lst[i] == result:
            print(final_sol_lst[i])

start_time = time.time()
solve()
end_time = time.time()
print('Time: ', end_time - start_time)