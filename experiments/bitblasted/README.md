This folder contains scripts to monitor OD of traces with 8-bit integers.
For RVHyper, we bitblast the traces


```
# Don't forget
source ../../venv/bin/activate
```

If there is no `hna` directory here, run

```
git submodule update --init
cd hna
cmake .
```

To re-generate the monitors, run the scripts `make prep`.
Check the script to see (or modify) the commands for generating the monitors.
The eHL monitor is generated into `ehl-8b` directory and the sHL monitor
into `shl-le` directory. Each of these directories contain en executable `monitor`
that is the actual compiled monitor.
