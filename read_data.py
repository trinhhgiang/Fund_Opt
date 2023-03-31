# import os
# print(os.getcwd())

def read_input_file(filename):
    with open(filename, 'r') as f:
        N, m, M = map(int, f.readline().split())
        d, s, e = [], [], []
        n = 0
        for line in f:
            di, si, ei = map(int, line.split())
            d.append(di)
            s.append(si)
            e.append(ei)
            n = max(n, ei)
        return N, m, M, d, s, e, n

# N, m, M, d, s, e, n = read_input_file('for_hust/fund_opt/data/data_5.txt')
# print(N, m, M, d, s, e, n)