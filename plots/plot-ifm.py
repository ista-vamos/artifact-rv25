#!/usr/bin/python3

import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from os.path import dirname, join
from shutil import which

TIMEOUT = 120

USE_LATEX = (which('latex') is not None)
FIGSIZE=(6,2.5)

######################################################################
# get data
######################################################################

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
if have_rvhyper:
    data = pd.concat([data, data_rvhyper[["mon", "traces_num", "Length of traces", "cputime", "Bits", "mem"]]], ignore_index=True)
if have_mpt:
    data = pd.concat([data, data_mpt[["mon", "traces_num", "Length of traces", "cputime", "Bits", "mem"]]], ignore_index=True)

######################################################################
# functions to generate the plot
######################################################################

def gen_fig(data, xcol, ycol, bits):
    if USE_LATEX:
        plt.rcParams['text.usetex'] = True

        data["Monitor"] = data["mon"].map(
        {
            "rvhyper"      : r"$\mathit{RVHyper}$",
            "ehl"          : r"$\mathit{eHL}$",
            "shl-le"       : r"$\mathit{sHL}$",
            "shl-eq"       : r"$\mathit{sHL_{=}}$",
            "mpt"          : r"$\mathit{MPT}$"
        }
        )
    else:
        print('WARNING: not using latex labels', file=sys.stderr)
        plt.rcParams['text.usetex'] = False

        data["Monitor"] = data["mon"].map(
            {
             "rvhyper"     : "RVHyper",
             "mpt"         : "MPT",
             "ehl"         : "eHL",
             "shl-le"      : "sHL<=",
             "shl-eq"      : "sHL=",
            }
        )

    _gen_fig(data, xcol, ycol, bits)


def _gen_fig(data, xcol, ycol, bits):
    fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)
    ax = [ax]
    selected_data = data[(data["Length of traces"].isin((1000, 2000, 3000))) & (data["Bits"] == bits)]
    plot1 = sns.lineplot(data=selected_data,
                         x=xcol, y=ycol,
                         hue="Length of traces", style="Monitor",
                         ax=ax[0], palette="bright",
                         markers=True, dashes=True,
                         errorbar=None
                         )
    ax[0].set(xlabel='Number of traces', ylabel='CPU time [s]',
              title=f'{bits}-bit alphabet')

    ax[0].legend(fontsize=7)

    fig.tight_layout()
    fig.savefig(f"plot.pdf", bbox_inches='tight', dpi=600)


######################################################################
# generate the plot
######################################################################

BITS=8
try:
    gen_fig(data, "traces_num", "cputime", BITS)
except RuntimeError as e:
    sys.stderr.flush()
    sys.stdout.flush()
    if str(e).strip().startswith("latex"):
        print('=================================================', file=sys.stderr)
        print('WARNING: failed using latex, trying again without', file=sys.stderr)
        USE_LATEX = False
        gen_fig(data, "traces_num", "cputime", BITS)



exit(0)

