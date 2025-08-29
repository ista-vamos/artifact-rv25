import sys
from statistics import mean

data = {}
with open(sys.argv[1], 'r') as f:
    for row in f:
        row = row.split()
        data.setdefault(row[0],{}).setdefault(int(row[1]), []).append(float(row[6]))


print("eHL")
for N, row in data['ehl'].items():
    print(N, mean(row))

print("sHL")
for N, row in data['shl'].items():
    print(N, mean(row))
