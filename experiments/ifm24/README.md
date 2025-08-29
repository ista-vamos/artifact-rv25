This folder contains scripts to reproduce the experiments with eHL from iFM'24
and adds new experiments with sHL that compare to the results of eHL.

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

To re-generate the monitors, run the script `generate.sh`.
Check the script to see (or modify) the commands for generating the monitors.
