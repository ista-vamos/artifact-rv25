#!/bin/bash

# before running this, you must generate the traces.
# # See `libhydrogen` subdirectory.

set -e

DIR=$(dirname $0)
HNA=$DIR/../../hna-ifm24

B=16
python -OO ${HNA}/hnl.py "$(cat traces-$B-ifm24/formula-stred.txt)" --csv-header "$(cat traces-$B-ifm24/header.txt)" \
  --out-dir mon-ehl --alphabet="7b" -DMEASURE_CPUTIME=OFF --reduction reflexive,symmetric -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
