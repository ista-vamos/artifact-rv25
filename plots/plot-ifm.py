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
if have_rvhyper:
    data = pd.concat([data, data_rvhyper[["mon", "traces_num", "Length of traces", "cputime", "Bits", "mem"]]], ignore_index=True)
if have_mpt:
    data = pd.concat([data, data_mpt[["mon", "traces_num", "Length of traces", "cputime", "Bits", "mem"]]], ignore_index=True)

data["Monitor"] = data["mon"].map(
    {"rvhyper" : r"$\mathit{RVHyper}",
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
trlen = 4000
xcol = "traces_num"
selected_data = data[(data["Length of traces"] == trlen)
                     & (data["Bits"].isin((2, 8, 10)))
                    ]
plot2 = sns.lineplot(data=selected_data,
                     x=xcol, y=ycol,
                     hue="Bits", style="Monitor",
                     ax=ax[1], palette="bright",
                     markers=True, dashes=True,
                     errorbar=None
                     )
ax[1].set(xlabel='Number of traces', ylabel='CPU time [s]',
          title=f'Traces length {trlen}')
ax[1].legend(fontsize=7,
             # loc='upper left', ncol=2, prop={'size':12}
            )

fig.tight_layout()
fig.savefig(f"plot-2.pdf", bbox_inches='tight', dpi=600)
######################################################################
fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)
ax = [ax]
xcol = "traces_num"
bt = 8
selected_data = data[(data["Length of traces"].isin((1000, 2000, 4000)))
                     & (data["Bits"] == bt)]
plot1 = sns.lineplot(data=selected_data,
                     x=xcol, y=ycol,
                     hue="Length of traces", style="Monitor",
                     ax=ax[0], palette="bright",
                     markers=True, dashes=True,
                     errorbar=None
                     )
ax[0].set(xlabel='Number of traces', ylabel='CPU time [s]',
          title=f'{bt}-bit alphabet')

ax[0].legend(fontsize=7,# ncol=2
             # loc='upper left', prop={'size':12}
            )


fig.tight_layout()
fig.savefig(f"plot-1.pdf", bbox_inches='tight', dpi=600)

# -------------------------
######################################################################
fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)
ax = [None, None, ax]

data_nost = data[data["mon"].isin(["ehl","shl-le","shl-eq"])]
data_nost = data_nost[["id", "Bits", "cputime", "Length of traces", "traces_num"]]

data_st = data[data["mon"].isin(["ehl-stred","shl-le-stred","shl-eq-stred"])]
data_st = data_st[["id", "Bits", "cputime", "Length of traces", "traces_num"]]



trlen = 1000

nost_d = data_nost.groupby("id").aggregate("mean")
st_d = data_st.groupby("id").aggregate("mean")
selected_data = st_d.join(nost_d, on="id", lsuffix="_st", rsuffix="_nost")
#print(selected_data[selected_data["Bits_st"] == 1][["cputime_st", "cputime_nost"]])
selected_data["cputime_st"] = selected_data["cputime_st"].fillna(value=TIMEOUT)
selected_data["cputime_nost"] = selected_data["cputime_nost"].fillna(value=TIMEOUT)
selected_data = selected_data[(selected_data["Length of traces_st"] == trlen)]
selected_data = selected_data[(selected_data["traces_num_st"] < 1000)]
selected_data["Bits"] = selected_data["Bits_st"].astype(int)
selected_data["traces_num"] = selected_data["traces_num_st"].astype(int)
sns.scatterplot(data=selected_data,
                x="cputime_st", y="cputime_nost",
                style="Bits", hue="traces_num",
                ax=ax[2], palette="bright",
                #markers=True, dashes=True,
                #errorbar=None
                )
xlim, ylim = ax[2].get_xlim(), ax[2].get_ylim()
m1 = 0
m2 = TIMEOUT
xlim = ylim = (m1, m2)
# ax[2].set_xlim(xlim)
# ax[2].set_ylim(ylim)


ax[2].plot(xlim, ylim, linestyle='--', color='k', lw=1, scalex=False, scaley=False)

#ax[2].set(yscale="symlog")

def rename(s):
    if s == "Bits_st": return "Bits"
    if s == "traces_num": return "# traces"
    return s

ax[2].set(xlabel='CPU time [s] (stutter red.)',
          ylabel='CPU time [s] (no stutter red.)',
          title=f"Traces length 1000")

h,l = ax[2].get_legend_handles_labels()
l = [rename(x) for x in l]
split=5
l1 = ax[2].legend(h[:split], l[:split], fontsize=7,
               loc='upper center')#, ncol=2)
l2 = ax[2].legend(h[split:],l[split:], loc='center right', fontsize=7)
ax[2].add_artist(l1)

fig.tight_layout()
fig.savefig(f"plot-3.pdf", bbox_inches='tight', dpi=600)


######################################################################
fig, ax = plt.subplots(1, 1, figsize=FIGSIZE)
ax = [None, None, ax]


trlen = 1000

nost_d = data_nost.groupby("id").aggregate("mean")
st_d = data_st.groupby("id").aggregate("mean")
selected_data = st_d.join(nost_d, on="id", lsuffix="_st", rsuffix="_nost")
#print(selected_data[selected_data["Bits_st"] == 1][["cputime_st", "cputime_nost"]])
selected_data["cputime_st"] = selected_data["cputime_st"].fillna(value=TIMEOUT)
selected_data["cputime_nost"] = selected_data["cputime_nost"].fillna(value=TIMEOUT)
selected_data = selected_data[(selected_data["Length of traces_st"] == trlen)]
#selected_data = selected_data[(selected_data["traces_num_st"] < 1000)]
selected_data["Bits"] = selected_data["Bits_st"].astype(int)
selected_data["traces_num"] = selected_data["traces_num_st"].astype(int)
#selected_data = selected_data[(selected_data["Bits"] > 1)]
sns.scatterplot(data=selected_data,
                x="cputime_st", y="cputime_nost",
                style="Bits", hue="traces_num",
                ax=ax[2], palette="bright",
                #markers=True, dashes=True,
                #errorbar=None
                )
xlim, ylim = ax[2].get_xlim(), ax[2].get_ylim()
m1 = 0
m2 = TIMEOUT
xlim = ylim = (m1, m2)
# ax[2].set_xlim(xlim)
# ax[2].set_ylim(ylim)
# 


ax[2].set(yscale="symlog")
ax[2].plot(xlim, ylim, linestyle='--', color='k', lw=1, scalex=False, scaley=False)

ax[2].set(xlabel='CPU time [s] (stutter red.)',
          ylabel='CPU time [s] (no stutter red.)',
          title=f"Traces length 1000")

h,l = ax[2].get_legend_handles_labels()
l = [rename(x) for x in l]
split=5
l1 = ax[2].legend(h[:split], l[:split], fontsize=7,
               loc='upper left')#, ncol=2)
l2 = ax[2].legend(h[split:],l[split:], loc='center right', fontsize=7)
ax[2].add_artist(l1)

fig.tight_layout()
fig.savefig(f"plot-4.pdf", bbox_inches='tight', dpi=600)

exit(0)

