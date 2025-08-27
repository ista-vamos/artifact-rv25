This folder contains scripts to monitor OD of traces with finite integers.
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

To re-generate the monitors, run the scripts `make`.
Check the script to see (or modify) the commands for generating the monitors.
