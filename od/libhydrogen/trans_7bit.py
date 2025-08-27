#!/usr/bin/env python3

import sys

N = 2**7
with open(sys.argv[1], 'r') as f:
    sys.stdout.write(f.readline())
    for row in f:
        row = row.split(',')
        new_row = [int(x) % N for x in row]
        print(','.join(map(str, new_row)))


