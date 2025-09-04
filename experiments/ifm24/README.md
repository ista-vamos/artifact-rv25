### Experiments on bit-blasted integers

This folder contains scripts to monitor OD of traces with 8-bit bit-blasted integers
(bit-blasting is necessary because we compare with RVHyper).

These are the experiments reported in Fig. 7 (top).

The experiments are the same as in the paper _Monitoring Extended Hypernode Logic (iFM'24)_,
but they add sHL monitors.
In short, we generate random traces with random 8-bit inputs (bit-blasted) and the last event containing
a random 8-bit output (see `gen-traces.py`).


### Running

Run `make short` for a short version of the experiments, `make full` for the full version
of the experiments. Results are stored into `results/out.csv` (overwritten each time
experiments are run).

Note that monitors are generated automatically when running `make full` or `make short`.
The eHL monitor is generated into `ehl-8b` directory and the sHL monitor
into `shl-le` directory. Each of these directories contains an executable `monitor`
that is the actual compiled monitor.


### Running manually

For tweaking the experiments, see `Makefile` and the help message of the script `run.py`.


#### In a nutshell 

- Before anything, do not forget to setup the virtual environment in the case
  you are in the out-of-docker build (something like `source ../../venv/bin/activate`).
- To (re-)generate the monitors, run scripts `generate-ehl.sh` and `generate-shl.sh`
  (see `Makefile` for the parameters or check the scripts themselves).
- To run the experiments, use `python3 run.py`. Again, check `Makefile` or the help message
  of `run.py` to see the parameters. For convenience, we put the help message of `run.py`
  here too:
  ```
  usage: run.py [-h] [-j PROC_NUM] [--out OUT] [--verbose] [--traces-lens TRACES_LENS] [--traces-nums TRACES_NUMS]
              [--bits BITS] [--trials TRIALS] [--timeout TIMEOUT] [--monitors MONITORS] [--one-trace]
              [--traces-no-stuttering]

  options:
    -h, --help            show this help message and exit
    -j PROC_NUM
    --out OUT             Name of the output file. Default is 'out.csv'
    --verbose             Print some extra messages
    --traces-lens TRACES_LENS
                          Comma-separated list of lenghts of traces
    --traces-nums TRACES_NUMS
                          Comma-separated list of numbers of traces
    --bits BITS           Comma-separated list of bits for the alphabet (not affecting mpt and shl monitors).
                          Supported are any combination of 1, 2, 4, 8, 10.
    --trials TRIALS       How many times repeat each run
    --timeout TIMEOUT     In seconds
    --monitors MONITORS   List of monitors: mpt, rvhyper, ehl, ehl-stred,shl-le,shl-eq,shl-le-stred,shl-eq-stred
    --one-trace           Make all traces same
    --traces-no-stuttering
                          Generate traces with no stuttering
  ```

Note that for each value `<B>` of BITS, you need to generate the eHL monitors with the command
```
./generate-ehl.sh <B>b
```

The monitor is generated into `ehl-<B>b` directory.
The default sHL monitor is `shl-le`, meaning that it uses "less or equal" comparisons in the formula.
Other monitors, like `shl-eq` (equalities for the comparison) and `shl-le-stred` (stutter-reduced less or equal)
can be used, but you must generate them. For this, uncomment generating these monitors in `generate-shl.sh`
(or `generate-ehl.sh` for eHL versions of the monitors).

