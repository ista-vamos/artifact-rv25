#!/bin/bash

set -e

DIR=$(dirname $0)
HNA=$DIR/../../hna-ifm24

FORMULA='forall t1, t2: (!(in(t1) <= in(t2) && in(t2) <= in(t1)) || (out(t1) <= out(t2) && out(t2) <= out(t1)))'
CSV_HEADER='in: uint64_t, out: uint64_t'

# NOTE: we do not measure cputime inside the monitors as this is handled externally by the `time` utility.
# Also, we do not cache the results here as for the OD formulas it has no effect and it only creates overhead.

ALPHABET=8b

if [ ! -z "$1" ]; then
  ALPHABET=$1
fi

python3 -OO $HNA/hnl.py "$FORMULA" \
    --out-dir ehl-$ALPHABET --csv-header="$CSV_HEADER" \
    --alphabet=$ALPHABET --overwrite-file $DIR/files/read_csv_event.h -DMEASURE_CPUTIME=OFF -DCACHE_ATOMS_RESULTS=OFF --reduction reflexive,symmetric


# FORMULA_STRED='forall t1, t2: (!([in(t1)] <= [in(t2)] && [in(t2)] <= [in(t1)]) || ([out(t1)] <= [out(t2)] && [out(t2)] <= [out(t1)]))'
# CSV_HEADER='in: uint64_t, out: uint64_t'
# for ALPHABET in 1b 2b 4b; do
#   python3 -OO $HNA/hnl.py "$FORMULA_STRED" \
#     --out-dir ehl-stred-$ALPHABET --csv-header="$CSV_HEADER" \
#     --alphabet=$ALPHABET --overwrite-file $DIR/files/read_csv_event.h -DMEASURE_CPUTIME=OFF -DCACHE_ATOMS_RESULTS=OFF --reduction reflexive,symmetric
# done
