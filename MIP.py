from ortools.linear_solver import pywraplp
import sys
import time
# N,m,M=8,10,14
# d=[6,8,3,1,5,7,2,4]
# s=[2,1,1,3,4,2,4,3]
# e=[4,2,3,4,5,3,5,5]

t1=time.time()
# N = 20
# n = 10
# m = 30
# M = 100
# d=[8,9,12,15,20,17,19,6,7,22,16,15,17,5,9,15,20,25,10,18]
# s=[2,5,3,1,4,4,5,2,4,3,2,3,2,1,4,5,4,1,2,3]
# e=[5,9,7,8,6,8,8,7,6,6,6,6,5,7,8,10,8,8,7,6]

def load_data(file):
    with open(file) as f:
        N,m,M=(int(i) for i in f.readline().split())
        d=[0]*N
        s=[0]*N
        e=[0]*N
        for _ in range(N):
            d[_],s[_],e[_]=(int(i) for i in f.readline().split())
    return N,m,M,d,s,e

data=sys.argv[1]
N,m,M,d,s,e=load_data(data)

max_day=max(e)

solver = pywraplp.Solver.CreateSolver('SCIP')

x={}
t={}
inf=solver.infinity()

ma=solver.IntVar(m,M,'ma')
mi=solver.IntVar(m,M,'mi')

for day in range(max_day):
    t[day]=solver.IntVar(0,1,f'Day {day}')
    for field in range(N):
        x[day,field]=solver.IntVar(0,1,f'x[{day}][{field}]')
        if day<s[field] or day>e[field]:
            solver.Add(x[day,field]==0)

for field in range(N):
    exact_one=solver.Constraint(1,1)
    for day in range(max_day):
        exact_one.SetCoefficient(x[day,field],1)

for day in range(max_day):
    lb=solver.Constraint(0,inf)
    ub=solver.Constraint(0,inf)
    lb.SetCoefficient(t[day],-m)
    ub.SetCoefficient(t[day],M)
    biggest=solver.Constraint(0,inf)
    biggest.SetCoefficient(ma,1)
    least=solver.Constraint(-M,inf)
    least.SetCoefficient(mi,-1)
    least.SetCoefficient(t[day],-M)
    for field in range(N):
        lb.SetCoefficient(x[day,field],d[field])
        ub.SetCoefficient(x[day,field],-d[field])
        least.SetCoefficient(x[day,field],d[field])
        biggest.SetCoefficient(x[day,field],-d[field])

obj=solver.Objective()
obj.SetCoefficient(ma,1)
obj.SetCoefficient(mi,-1)
obj.SetMinimization()

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print('Objective value =', int(solver.Objective().Value()))
    for day in range(max_day):
        for field in range(N):
            print(int(x[day,field].solution_value()),end=' ')
        print()
    # print('Problem solved in %f milliseconds' % solver.wall_time())
    # print('Problem solved in %d iterations' % solver.iterations())
    # print('Problem solved in %d branch-and-bound nodes' % solver.nodes())
else:
    print('The problem does not have an optimal solution.')

t2=time.time()
print("Time: ",end='')
print(round(t2-t1,2))

