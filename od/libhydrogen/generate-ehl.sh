#!/bin/bash

# before running this, you must generate the traces.
# # See `libhydrogen` subdirectory.

set -e

DIR=$(dirname $0)
HNA=$DIR/../../hna-ifm24

B=16
python -OO ${HNA}/hnl.py "$(cat traces-$B/formula-stred.txt)" --csv-header "$(cat traces-$B/header.txt)" \
  --out-dir traces-$B/monitor --alphabet="7b" -DMEASURE_CPUTIME=OFF --reduction reflexive,symmetric
