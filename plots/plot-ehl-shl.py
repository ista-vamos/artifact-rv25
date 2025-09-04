#!/usr/bin/python3

import sys
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from shutil import which

TIMEOUT = 120

USE_LATEX = (which('latex') is not None)
FIGSIZE=(6,2.5)

######################################################################
# get data
######################################################################
data_hnl = pd.read_csv(sys.argv[1], sep=" ")
data_hnl.columns = ["mon", "id", "traces_num", "Length of traces", "Bits", "verdict", "instances", "atoms", "reused_monitors", "reused_verdicts", "cputime", "walltime", "mem", "returncode"]
data_hnl.replace({"None": None}, inplace=True)

data = data_hnl

######################################################################
# functions to generate the plot
######################################################################

def _gen_fig(data, xcol, ycol, trlen):
    fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)
    ax = [None, ax]
    selected_data = data[(data["mon"].isin(["ehl", "shl-le"]))]
    plot2 = sns.lineplot(data=selected_data,
                         x=xcol, y=ycol,
                         hue="Bits", style="Monitor",
                         ax=ax[1], palette="bright",
                         markers=True, dashes=True,
                         errorbar=None
                         )
    ax[1].set(xlabel='Number of traces', ylabel='CPU time [s]')
    ax[1].legend(fontsize=7)

    fig.tight_layout()
    fig.savefig(f"plot.pdf", bbox_inches='tight', dpi=600)

def gen_fig(data, xcol, ycol, trlen):
    if USE_LATEX:
        plt.rcParams['text.usetex'] = True

        data["Monitor"] = data["mon"].map(
            {
             "ehl"          : r"$\mathit{eHL}$",
             "shl-le"       : r"$\mathit{sHL}$"
            }
        )
    else:
        print('WARNING: not using latex labels', file=sys.stderr)
        plt.rcParams['text.usetex'] = False

        data["Monitor"] = data["mon"].map(
            {
             "ehl"          : "eHL",
             "shl-le"       : "sHL<=",
            }
        )

    _gen_fig(data, xcol, ycol, trlen)



######################################################################
# generate the plot
######################################################################

try:
    gen_fig(data, "traces_num", "cputime", 3000)
except RuntimeError as e:
    sys.stderr.flush()
    sys.stdout.flush()
    if str(e).strip().startswith("latex"):
        print('=================================================', file=sys.stderr)
        print('WARNING: failed using latex, trying again without', file=sys.stderr)
        USE_LATEX = False
        gen_fig(data, "traces_num", "cputime", 3000)

exit(0)

