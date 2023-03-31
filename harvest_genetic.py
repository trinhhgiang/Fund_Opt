import random
import itertools
import time

import sys
from read_data import*

data=sys.argv[1]
N, m, M, d, s, e, n=read_input_file(data)
# N = 8
# n = 5
# m = 10
# M = 14
# d = [6, 8, 3, 1, 5, 7, 2, 4]
# s = [2, 1, 1, 3, 4, 2, 4, 3]
# e = [4, 2, 3, 4, 5, 3, 5, 5]

# N = 20
# n = 10
# m = 30
# M = 100
# d=[8,9,12,15,20,17,19,6,7,22,16,15,17,5,9,15,20,25,10,18]
# s=[2,5,3,1,4,4,5,2,4,3,2,3,2,1,4,5,4,1,2,3]
# e=[5,9,7,8,6,8,8,7,6,6,6,6,5,7,8,10,8,8,7,6]

def genetic_algorithm(number_of_generations, population_size, elite_size):
    population = generate_initial_population(population_size)
    for _ in range(number_of_generations):
        population_loss = loss_evaluate(population)
        population, population_loss = sort_by_loss(population, population_loss)
        mating_pool = select_mating_pool(elite_size, population)
        offspring = breeding(mating_pool)
        population = replace_worst(population, offspring)
        population, population_loss = sort_by_loss(population, population_loss)
    return best_individual(population, population_loss)

def optimization_dev(sol):
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

def generate_random_individual():
    lst = []
    for i in range(N):
        lst.append(random.randrange(s[i], e[i]+1))
    idx = 1
    individual = [[] for _ in range(n)]
    for i in lst:
        individual[i-1].append(idx)
        idx += 1
    return individual

def generate_initial_population(population_size):
    population = []
    for _ in range(population_size):
        individual = generate_random_individual()
        population.append(individual)
    return population

def loss_evaluate(population):
    population_loss = []
    for individual in population:
        loss = 0
        for i in individual:
            _sum = 0
            for j in i:
                _sum += d[j-1]
            if _sum == 0:
                continue
            loss += max(m - _sum, 0) + max(_sum - M ,0)
        population_loss.append(loss)
    return population_loss

def sort_by_loss(population, population_loss):
    population_loss, population = zip(*sorted(zip(population_loss, population)))
    population = list(population)
    population_loss = list(population_loss)
    return population, population_loss

def select_mating_pool(elite_size, population):
    mutation = random.sample(population[elite_size:], 1)
    mating_pool = random.sample(population[:elite_size]+mutation, 2)
    return mating_pool

def breeding(mating_pool):
    offspring = []
    while len(list(itertools.chain(*offspring))) < N:
        offspring = []
        for i in range(0, n):
            check = list(itertools.chain(*offspring))
            gene1 = mating_pool[0][i]
            gene2 = mating_pool[1][i]
            k = 0
            for j in gene1:
                if j in check:
                    k = 1
                    offspring.append(gene2)
                    break
            for j in gene2:
                if j in check:          
                    k = 1
                    offspring.append(gene1)
                    break
            if k == 0:
                offspring.append(*random.sample([gene1, gene2], 1))
    return offspring

def replace_worst(population, offspring):
    population[-1] = offspring[:]
    return population

def best_individual(population, population_loss):
    return population[0], population_loss[0]

def solve():
    feasible_lst = []
    number_of_population = 70
    number_of_generations = 10
    population_size = 10
    elite_size = 4
    for _ in range(number_of_population):
        individual, loss = genetic_algorithm(number_of_generations, population_size, elite_size)
        if loss == 0:
            feasible_lst.append(individual)
    dev_lst = []
    for sol in feasible_lst:
        dev_lst.append(optimization_dev(sol))
    print('Feasible solutions:')
    print(feasible_lst)
    print('Deviations:')
    print(dev_lst)
    print('Optimal value:')
    opt_val = min(dev_lst)
    print(opt_val)
    print('Optimal solution:', )
    print(feasible_lst[dev_lst.index(opt_val)])

start_time = time.time()
solve()
end_time = time.time()
print('Time: ', end_time - start_time)
