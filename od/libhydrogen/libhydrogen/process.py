import sys

FILE=sys.argv[1]

variables = {}
in_var_num = 0
out_var_num = 0

def get_var(s):
    for addrs, name in variables.items():
        if s >= addrs[0] and s < addrs[1]:
            return name
    #print(f"Could find {s}-{e}")
    return None

def handle_var(line, ty):
    assert ty in ("OUT", "IN"), ty

    #VAR start-addr end-addr
    addr_start = int(line[1], base=16)
    addr_end = int(line[2], base=16)
    assert all((get_var(ptr) is None for ptr in range(addr_start, addr_end)))

    global variables
    name = "o" if ty == "OUT" else "i"
    if name == "o":
        global out_var_num
        out_var_num += 1
        var_num = out_var_num
    else:
        global in_var_num
        in_var_num += 1
        var_num = in_var_num

    for i, addr in enumerate(range(addr_start, addr_end)):
        variables[(addr, addr + 1)] = f"{name}{var_num}_{i}"

def update_val(line, values):
    #VAL start-addr end-addr val
    
    # XXX: we assume no partial writes
    addr_start = int(line[1], base=16)
    addr_end = int(line[2], base=16)

    name = variables[(addr_start, addr_end)]
    values[name] = line[3]

def print_state(values, names):
    #print(', '.join((f"{name} = {values[name]}" for name in names)))
    print(','.join((str(values[name]) for name in names)))

# gather the variables first
with open(FILE, 'r') as f:
    for line in f:
        parts = line.split()
        if parts[0] in ('OUT', 'IN'):
            handle_var(parts, parts[0])

#print(variables)

# now transform the file into CSV
with open(FILE, 'r') as f:
    # fix the order of variables
    names = list(variables.values())
    # we need to track the current value of all variables
    values = {}
    for name in names:
        values[name] = 0

    print(','.join(names))

    for line in f:
        parts = line.split()
        if parts[0] == 'VAL':
            update_val(parts, values)
            print_state(values, names)

with open('header.txt', 'w') as h:
    print(','.join((f"{n}:unsigned" for n in names)), file=h)

with open('formula.txt', 'w') as h:
    ins = [n for n in names if n.startswith('i')]
    outs = [n for n in names if n.startswith('o')]
    I = [f"({v}(t1) <= {v}(t2) && {v}(t2) <= {v}(t1))" for v in ins]
    in_f = I[0]
    for f in I[1:]:
        in_f = f"({in_f} && {f})"

    O = [f"({v}(t1) <= {v}(t2) && {v}(t2) <= {v}(t1))" for v in outs]
    out_f = O[0]
    for f in O[1:]:
        out_f = f"({out_f} && {f})"

    print(f"forall t1, t2: !({in_f}) || {out_f}", file=h)

with open('formula-stred.txt', 'w') as h:
    ins = [n for n in names if n.startswith('i')]
    outs = [n for n in names if n.startswith('o')]
    I = [f"([{v}(t1)] <= [{v}(t2)] && [{v}(t2)] <= [{v}(t1)])" for v in ins]
    in_f = I[0]
    for f in I[1:]:
        in_f = f"({in_f} && {f})"

    O = [f"([{v}(t1)] <= [{v}(t2)] && [{v}(t2)] <= [{v}(t1)])" for v in outs]
    out_f = O[0]
    for f in O[1:]:
        out_f = f"({out_f} && {f})"

    print(f"forall t1, t2: !({in_f}) || {out_f}", file=h)



