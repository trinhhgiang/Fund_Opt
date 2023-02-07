from ortools.sat.python import cp_model
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
model=cp_model.CpModel()

x={}

for day in range(1,max_day+1):
    for field in range(N):
        x[day,field]=model.NewBoolVar(f"x[{day},{field}]")
        if day>e[field] or day<s[field]:
            model.Add(x[day,field]==0)

for field in range(N):
    model.AddExactlyOne(x[day, field] for day in range(1,max_day+1))


for day in range(1,max_day+1):
    b=model.NewBoolVar('b')
    model.Add(
        sum(x[day,field]*d[field] for field in range(N)) < m
    ).OnlyEnforceIf(b)
    model.Add(
        sum(x[day,field]*d[field] for field in range(N)) >= m
    ).OnlyEnforceIf(b.Not())
    model.Add(
        sum(x[day,field]*d[field] for field in range(N)) <= M
    )
    for field in range(N):
        model.Add(x[day,field]==0).OnlyEnforceIf(b)

x_max=model.NewIntVar(m,M,'x_max')
x_min=model.NewIntVar(m,M,'x_min')
for day in range(1,max_day+1):
    s=sum(x[day,field]*d[field] for field in range(N))
    model.Add(x_max>=s)
    b=model.NewBoolVar('b')
    model.Add(s!=0).OnlyEnforceIf(b)
    model.Add(s==0).OnlyEnforceIf(b.Not())
    model.Add(x_min<=s).OnlyEnforceIf(b)

model.Minimize(x_max-x_min)
solver=cp_model.CpSolver()
status=solver.Solve(model)

if status==cp_model.OPTIMAL:
    for day in range(1,max_day+1):
        for field in range(N):

            print(solver.Value(x[day,field]),end=' ')

        print()
    print(solver.Value(x_max)-solver.Value(x_min))

t2=time.time()
print("Time: ",end='')
print(round(t2-t1,2))