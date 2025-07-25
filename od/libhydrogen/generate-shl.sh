#!/bin/bash

# IMPORTANT: before running this, you must generate the traces. See README.

set -e

DIR=$(dirname $0)
HNA=$DIR/../../hna

FORMULA='forall t1, t2: (!(([in0(t1)]  = [in0(t2)]) && ([in1(t1)] = [in1(t2)])) ||
  (((([out0(t1)] = [out0(t2)]) && ([out1(t1)] = [out1(t2)])) && ([out2(t1)] = [out2(t2)])) && ([out3(t1)] = [out3(t2)])))'
CSV_HEADER='in0: uint64_t, in1: uint64_t, out0: uint64_t, out1: uint64_t, out2: uint64_t, out3: uint64_t'

# NOTES: we do not measure cputime inside the monitors as this is handled externally by the `time` utility.
# Also, we do not cache the results here as for the OD formulas it has no effect and it only creates overhead.

python3 -OO $HNA/hnl.py "$FORMULA" \
  --out-dir mon --data="$CSV_HEADER" -DMEASURE_CPUTIME=OFF -DCACHE_ATOMS_RESULTS=OFF --logic shl --reduction reflexive,symmetric
