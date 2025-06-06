#!/usr/bin/python3

import sys
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from statistics import mean
import pandas as pd
import seaborn as sns
from os.path import basename, dirname, join

TIMEOUT = 120

data = pd.read_csv(sys.argv[1], sep=" ")
data.columns = ["mon", "traces_num", "bytes", "verdict", "instances", "atoms", "cputime", "walltime", "mem", "returncode"]
data.replace({"None": None}, inplace=True)

D = data[["traces_num", "bytes", "atoms", "cputime", "mem"]]
print(D.groupby(["bytes", "traces_num"]).mean())

exit(0)

