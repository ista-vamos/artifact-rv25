#!/bin/bash

set -e

DIR=$(dirname $0)
HNA=$DIR/../../hna

FORMULA='forall t1, t2: (!(in(t1) <= in(t2) && in(t2) <= in(t1)) || (out(t1) <= out(t2) && out(t2) <= out(t1)))'
CSV_HEADER='in: uint64_t, out: uint64_t'

# NOTES: we do not measure cputime inside the monitors as this is handled externally by the `time` utility.
# Also, we do not cache the results here as for the OD formulas it has no effect and it only creates overhead.

python3 -OO $HNA/hnl.py "$FORMULA" \
  --out-dir shl-le --data="$CSV_HEADER" \
  --alphabet=$ALPHABET --overwrite-file $DIR/files/read_csv_event.h -DMEASURE_CPUTIME=OFF -DCACHE_ATOMS_RESULTS=OFF --logic shl\
  --reduction reflexive,symmetric

# FORMULA_STRED='forall t1, t2: (!([in(t1)] <= [in(t2)] && [in(t2)] <= [in(t1)]) || ([out(t1)] <= [out(t2)] && [out(t2)] <= [out(t1)]))'
# FORMULA_EQ='forall t1, t2: (!(in(t1) = in(t2)) || (out(t1) = out(t2)))'
# FORMULA_STRED_EQ='forall t1, t2: (!([in(t1)] = [in(t2)]) || ([out(t1)] = [out(t2)]))'
#
# python3 -OO $HNA/hnl.py "$FORMULA_STRED" \
#   --out-dir shl-le-stred --data="$CSV_HEADER" \
#   --alphabet=$ALPHABET --overwrite-file $DIR/files/read_csv_event.h -DMEASURE_CPUTIME=OFF -DCACHE_ATOMS_RESULTS=OFF --logic shl\
#   --reduction reflexive,symmetric
# 
# python3 -OO $HNA/hnl.py "$FORMULA_EQ" \
#   --out-dir shl-eq --data="$CSV_HEADER" \
#   --alphabet=$ALPHABET --overwrite-file $DIR/files/read_csv_event.h -DMEASURE_CPUTIME=OFF -DCACHE_ATOMS_RESULTS=OFF --logic shl\
#   --reduction reflexive,symmetric
# 
# python3 -OO $HNA/hnl.py "$FORMULA_STRED_EQ" \
#   --out-dir shl-eq-stred --data="$CSV_HEADER" \
#   --alphabet=$ALPHABET --overwrite-file $DIR/files/read_csv_event.h -DMEASURE_CPUTIME=OFF -DCACHE_ATOMS_RESULTS=OFF --logic shl\
#   --reduction reflexive,symmetric
