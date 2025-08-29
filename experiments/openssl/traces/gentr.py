#!/usr/bin/env python3

import sys

read_size = int(sys.argv[1])
fin = open(sys.argv[2], 'rb')
fout = open(sys.argv[3], 'rb')

# we output it from low to high bits, but that does not matter much
def to_bits(I, O, b):
    mask = 2**b - 1
    blocks = int(8 / b)
    for n in range(blocks):
        yield (I & mask), (O & mask)
        I = I >> b
        O = O >> b



print('in,out')

if read_size >= 8:
    read_size = int(read_size/8)
    while True:
        I, O = b'', b''
        if fin:
            I = fin.read(read_size)
            if I == b'':
                fin = None
                if fout is None:
                    break
        if fout:
            O = fout.read(read_size)
            if O == b'':
                fout = None
                if fin is None:
                    break

        print(f'{int.from_bytes(I)},{int.from_bytes(O)}')
else:
    assert read_size == 1 or read_size % 2 == 0
    while True:
        I, O = b'', b''
        if fin:
            I = fin.read(1)
            if I == b'':
                fin = None
                if fout is None:
                    break
        if fout:
            O = fout.read(1)
            if O == b'':
                fout = None
                if fin is None:
                    break

        for i, o in to_bits(int.from_bytes(I), int.from_bytes(O), read_size):
            print(f'{i},{o}')
