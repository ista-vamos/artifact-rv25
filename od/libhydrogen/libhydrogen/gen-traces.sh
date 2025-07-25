#!/bin/bash

LEN=$1
NUM=$2
OUTDIR=$3

HNL=$4

if [ -z $LEN -o -z $NUM -o -z $OUTDIR ]; then
	echo "Usage: $0 <length of input> <number of traces> <output dir> [hnl-script path]" 1>&2
	echo "The number of traces is per one process, so the total number of traces is two times more"
	echo "If the path to the 'hnl' script is given, the monitor is generated too"
	exit 1
fi


cd $(dirname $0)
mkdir -p $OUTDIR

for i in $(seq 1 $NUM); do
	INPUT=$(tr -dc A-Za-z0-9 </dev/urandom | head -c $LEN; echo)
	./hydro_hash $INPUT 1>/dev/null
	python ./process.py out.tr > "$OUTDIR/$i.tr"

	./hydro_hash-opt $INPUT 1>/dev/null
	python ./process.py out.tr > "$OUTDIR/$i-opt.tr"
done

cp header.txt formula.txt formula-stred.txt "$OUTDIR"


