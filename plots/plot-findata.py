#!/usr/bin/python3

import sys
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from statistics import mean
import pandas as pd
import seaborn as sns
from os.path import basename, dirname, join

plt.rcParams['text.usetex'] = True

TIMEOUT = 120

have_rvhyper=False
have_mpt=False
have_hnl=False
with open(sys.argv[1], "r") as f,\
     open(join(dirname(__file__), "_rvhyper.csv"), "w") as f_rh,\
     open(join(dirname(__file__), "_hnl.csv"), "w") as f_hnl,\
     open(join(dirname(__file__), "_mpt.csv"), "w") as f_m:
    for line in f:
        if line.startswith("rvhyper"):
            have_rvhyper = True
            f_rh.write(line)
        elif line.startswith("mpt"):
            have_mpt = True
            f_m.write(line)
        elif line.startswith("ehl") or line.startswith("shl"):
            have_hnl = True
            f_hnl.write(line)
        else:
            raise RuntimeError(f"Invalid line: {line}")

if have_rvhyper:
    data_rvhyper = pd.read_csv("_rvhyper.csv", sep=" ")
    data_rvhyper.columns = ["mon", "id", "traces_num", "Length of traces", "Bits", "cputime", "walltime", "mem", "returncode"]
    data_rvhyper.replace({"None": None}, inplace=True)

if have_mpt:
    data_mpt = pd.read_csv("_mpt.csv", sep=" ")
    data_mpt.columns = ["mon", "id", "traces_num", "Length of traces", "Bits", "wbg_size", "cputime", "walltime", "mem", "returncode"]
    data_mpt.replace({"None": None}, inplace=True)

data_hnl = pd.read_csv("_hnl.csv", sep=" ")
data_hnl.columns = ["mon", "id", "traces_num", "Length of traces", "Bits", "verdict", "instances", "atoms", "reused_monitors", "reused_verdicts", "cputime", "walltime", "mem", "returncode"]
data_hnl.replace({"None": None}, inplace=True)

data = data_hnl
# if have_rvhyper:
#     data = pd.concat([data, data_rvhyper[["mon", "traces_num", "Length of traces", "cputime", "Bits", "mem"]]], ignore_index=True)
# if have_mpt:
#     data = pd.concat([data, data_mpt[["mon", "traces_num", "Length of traces", "cputime", "Bits", "mem"]]], ignore_index=True)

data["Monitor"] = data["mon"].map(
    {"rvhyper" : r"$\mathit{RVHyper}$",
     "ehl" : r"$\mathit{eHL}$",
     "ehl-stred" : r"$\mathit{eHL_{sr}}$",
     "shl-le" : r"$\mathit{sHL}$",
     "shl-eq" : r"$\mathit{sHL}$",
     "shl-el-stred" : r"$\mathit{sHL_{sr}}$",
     "shl-eq-stred" : r"$\mathit{sHL_{sr}}$",
     "mpt": r"$\mathit{MPT}$"}
)


FIGSIZE=(6,3)
ycol = "cputime"
######################################################################
fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)
ax = [None, ax]
trlen = 3000
xcol = "traces_num"
selected_data = data[#(data["Length of traces"] == trlen) &
                     (data["mon"].isin(["ehl", "shl-le"]))]
plot2 = sns.lineplot(data=selected_data,
                     x=xcol, y=ycol,
                     hue="Bits", style="Monitor",
                     ax=ax[1], palette="bright",
                     markers=True, dashes=True,
                     errorbar=None
                     )
ax[1].set(xlabel='Number of traces', ylabel='CPU time [s]'
          #title=f'Traces length {trlen}'
          )
ax[1].legend(fontsize=7,
             # loc='upper left', ncol=2, prop={'size':12}
            )

fig.tight_layout()
fig.savefig(f"plot.pdf", bbox_inches='tight', dpi=600)
######################################################################
exit(0)

