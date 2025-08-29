#!/usr/bin/env python3

import sys
from functools import reduce

def qword_chunks (inp: list):
    for i in range(0, len(inp), 8):
        yield inp[i:i+8]

f = open(sys.argv[1], 'r')

old_header = f.readline().split(',')

def chunk_to_qword(chunk):
    assert len(chunk) == 8, chunk
    return reduce(lambda x, y: x | y, map(lambda t: int(t[0]) << t[1], zip(chunk, range(0, 64, 8))), 0)

###
# Generate the header
###
i_n = 0
o_n = 0
header = []
for chunk in qword_chunks(old_header):
    assert len(chunk) == 8
    assert (all(s.startswith('i') for s in chunk) or all(s.startswith('o') for s in chunk)), chunk
    if chunk[0].startswith('i'):
        header.append(f'in{i_n}')
        i_n += 1
    elif chunk[0].startswith('o'):
        header.append(f'out{o_n}')
        o_n += 1
    else:
        raise RuntimeError(f"Invalid chunk: {chunk}")

print(','.join(header))

###
# Generate the numbers
###
for row in f:
    row = row.split(',')
    new_row = []
    for chunk in qword_chunks(row):
        new_row.append(chunk_to_qword(chunk))

    print(','.join(map(str, new_row)))
f.close()


