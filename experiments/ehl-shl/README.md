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
