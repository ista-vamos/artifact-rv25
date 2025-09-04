This folder contains scripts to monitor Async OD of traces generated from OpenSSL. 

These are the experiments reported in Table 1.

## Running

If you built the artifact manually outside docker, don't forget to run:
```
source ../../venv/bin/activate
```

There are two versions of experiments:

 - `make full`    full experiments
 - `make short`   short version of experiments

The monitor is generated automatically when running `make full` or `make short`
into the `shl-eq` directory.
The directory contains an executable `monitor` that is the actual
compiled monitor.

Check the scripts to see (or modify) the commands for generating the monitors.

## Traces

The traces are in the `traces` sub-directory, see the README in that sub-directory.

