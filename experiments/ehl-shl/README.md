# Comparing eHL and sHL monitors

These experiments compare eHL and sHL monitors on `n`-bit integers.
In short, we generate random traces with random `n`-bit inputs and the last
event containing a random `n`-bit output (see `gen-traces.py`).

These are the experiments reported in Fig. 7 (bottom).

## Running

If you built the artifact manually outside docker, don't forget to run:
```
source ../../venv/bin/activate
```

There are two versions of experiments:

 - `make full`    full experiments
 - `make short`   short version of experiments

Monitors are generated automatically when running `make full` or `make short`.
The eHL monitors are generated into `ehl-<B>b` directory where `<B>` is the number
of bits, and the sHL monitor into the `shl-le` directory.
Each of these directories contain en executable `monitor` that is the actual
compiled monitor.

Check the scripts to see (or modify) the commands for generating the monitors.

## Running experiments with custom bitwidths

You can manually run experiments with a chosen bit-width with:
```
BITWIDTH=6

# generate monitors
./generate-ehl.sh ${BITWIDTH}b
./generate-shl.sh

# run experiments
python3 ./run.py --bits=$BITWIDTH --traces-nums=1000,2000 --traces-lens=1000,3000 --trials=1
```

The eHL monitor is generated into the directory `ehl-${BITWIDTH}b`.
Check the help of `run.py` for tweaking more parameters.
