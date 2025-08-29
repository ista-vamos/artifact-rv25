# Comparing eHL and sHL monitors

This folder contains scripts to monitor OD of traces with 8-bit bit-blasted integers.
Bit-blasting is necessary because we compare with RVHyper.

These are the experiments reported in Fig. 7 bottom.

## Running

If you built the artifact manually outside docker, don't forget to run:
```
source ../../venv/bin/activate
```

There are two versions of experiments:

 - `make run`         full experiments
 - `make run-short`   short version of experiments

Monitors are generated automatically when running `make run` or `make run-short`.
The eHL monitor is generated into `ehl-8b` directory and the sHL monitor
into `shl-le` directory. Each of these directories contain en executable `monitor`
that is the actual compiled monitor.

Check the scripts to see (or modify) the commands for generating the monitors.

# Running experiments with custom bitwidths

You can manually run experiments with a chosen bit-width with:
```
BITWIDTH=6

# generate monitors
./generate-ehl.sh ${BITWIDTH}b
./generate-shl.sh

# run experiments
python3 ./run.py --bits=$BITWIDTH --traces-nums=1000,2000 --traces-lens=1000,3000 --trials=1
```
