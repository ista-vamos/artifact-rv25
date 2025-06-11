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

TIMEOUT = 400

data = pd.read_csv(sys.argv[1], sep=",")
data.columns = ["mon", "bits", "time"]
data.replace({"None": None}, inplace=True)

data["Monitor"] = data["mon"].map(
    {"rvhyper" : r"$\mathit{RVHyper}$",
     "ehl" : r"$\mathit{eHL}$",
     "ehl-stred" : r"$\mathit{eHL_{sr}}$",
     "ehl-lto" : r"$\mathit{eHL}^{\mathit{LTO}}$",
     "ehl-stred-lto" : r"$\mathit{eHL_{sr}}^{\mathit{LTO}}$"
    }
)


FIGSIZE=(3,3)
ycol = "cputime"
######################################################################
fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)
ax = [None, ax]
xcol = "bits"
ycol = "time"
plot2 = sns.lineplot(data=data,
                     x=xcol, y=ycol,
                     hue="Monitor", style="Monitor",
                     ax=ax[1], palette="bright",
                     markers=True, dashes=True,
                     errorbar=None
                     )
ax[1].set(xlabel='Number of bits', ylabel='CPU time [s]'
          #title=f'Traces length {trlen}'
          )
ax[1].legend(fontsize=7,
             # loc='upper left', ncol=2, prop={'size':12}
            )
plt.text(1.6, 380, r'$\mathit{sHL}^{LTO}: 8.8s$', fontsize=7)
plt.text(1.6, 355, r'$\mathit{sHL_{sr}}^{LTO}: 9.4s$', fontsize=7)
plt.text(1.6, 330, r'$\mathit{sHL_{sr}}: 9.2s$', fontsize=7)
plt.text(1.6, 305, r'$\mathit{sHL}: 9.2s$', fontsize=7)
fig.tight_layout()
fig.savefig(f"plot.pdf", bbox_inches='tight', dpi=600)
######################################################################
exit(0)

