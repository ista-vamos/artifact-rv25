#!/usr/bin/env python3

import datetime
from tempfile import mkdtemp
from subprocess import Popen, PIPE, DEVNULL, run as runcmd, TimeoutExpired
from os.path import dirname, realpath, basename, abspath, join, isfile, isdir
import os
from os import listdir, access, X_OK, environ as ENV, symlink, makedirs
from sys import argv, stderr, stdout
from multiprocessing import Pool
from shutil import rmtree
import signal

import argparse

bindir = f"{dirname(realpath(__file__))}/"

def errlog(*args):
    with open(join(dirname(__file__), "log.txt"), "a") as logf:
        for a in args:
            print(a, file=logf)

def run_one(arg):
    traces_num, nbytes, args = arg

    #print(f"  \033[37;1m.. [{datetime.datetime.now().time()}] running # traces = {traces_num}, nbytes = {nbytes}\033[0m", file=stderr)
    #stderr.flush()

    results = []
    if "shl" in args.monitors:
        results.append(run_shl(arg))
    if "ehl" in args.monitors:
        results.append(run_ehl(arg))

    return results


def run_shl(arg):
    traces_num, nbytes, args = arg
    mon_dir = f"{bindir}/mon"
    traces_dir = f"{bindir}/traces-{nbytes}/traces-{traces_num}"
    files = [join(traces_dir, fl) for fl in listdir(traces_dir) if fl.endswith(".tr")]

    cmd = ["/bin/time", "-f", '%Uuser %Ssystem %eelapsed %PCPU (%Xavgtext+%Davgdata %Mmaxresident)k',
           join(mon_dir, "monitor")]
    cmd += files
    p = Popen(cmd, stderr=PIPE, stdout=PIPE, preexec_fn=os.setsid)
    try:
        out, err = p.communicate(timeout=args.timeout)
    except TimeoutExpired:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        out, err = p.communicate(timeout=10)
    assert err is not None, cmd

    cpu_time=None
    wall_time=None
    mem=None
    instances, atoms, reused_mons, reused_verdicts = None, None, None, None
    verdict = None
    if p.returncode in (0, 1):
        for line in out.splitlines():
            line = line.strip()
            if line.startswith(b"Total formula"):
                instances = int(line.split()[3])
            elif line.startswith(b"Total atom"):
                atoms = int(line.split()[3])
            elif line.startswith(b"Reused monitors"):
                reused_mons = int(line.split()[2])
            elif line.startswith(b"Reused verdicts"):
                reused_verdicts = int(line.split()[2])
            elif b'TRUE' in line:
                verdict = 'TRUE'
            elif b'FALSE' in line:
                verdict = 'FALSE'

        for line in err.splitlines():
            if b"elapsed" in line:
                parts = line.split()
                assert b"user" in parts[0]
                assert b"elapsed" in parts[2]
                assert b"maxresident" in parts[5]
                cpu_time = float(parts[0][:-4])
                wall_time = float(parts[2][:-7])
                mem = int(parts[5][:-13])/1024.0
    else:
        errlog("Faield running HNL monitor:", out, err)

    return ("shl", traces_num, nbytes, verdict, instances, atoms, cpu_time, wall_time, mem, p.returncode)


def run_ehl(arg):
    traces_num, nbytes, args = arg
    mon_dir = f"{bindir}/mon-ehl"
    traces_dir = f"{bindir}/traces-{nbytes}-ifm24/traces-{traces_num}"
    files = [join(traces_dir, fl) for fl in listdir(traces_dir) if fl.endswith(".tr")]

    cmd = ["/bin/time", "-f", '%Uuser %Ssystem %eelapsed %PCPU (%Xavgtext+%Davgdata %Mmaxresident)k',
           join(mon_dir, "monitor")]
    cmd += files
    p = Popen(cmd, stderr=PIPE, stdout=PIPE, preexec_fn=os.setsid)
    try:
        out, err = p.communicate(timeout=args.timeout)
    except TimeoutExpired:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        out, err = p.communicate(timeout=10)
    assert err is not None, cmd

    cpu_time=None
    wall_time=None
    mem=None
    instances, atoms, reused_mons, reused_verdicts = None, None, None, None
    verdict = None
    if p.returncode in (0, 1):
        for line in out.splitlines():
            line = line.strip()
            if line.startswith(b"Total formula"):
                instances = int(line.split()[3])
            elif line.startswith(b"Total atom"):
                atoms = int(line.split()[3])
            elif line.startswith(b"Reused monitors"):
                reused_mons = int(line.split()[2])
            elif line.startswith(b"Reused verdicts"):
                reused_verdicts = int(line.split()[2])
            elif b'TRUE' in line:
                verdict = 'TRUE'
            elif b'FALSE' in line:
                verdict = 'FALSE'

        for line in err.splitlines():
            if b"elapsed" in line:
                parts = line.split()
                assert b"user" in parts[0]
                assert b"elapsed" in parts[2]
                assert b"maxresident" in parts[5]
                cpu_time = float(parts[0][:-4])
                wall_time = float(parts[2][:-7])
                mem = int(parts[5][:-13])/1024.0
    else:
        errlog("Faield running HNL monitor:", out, err)

    return (f"ehl", traces_num, nbytes, verdict, instances, atoms, cpu_time, wall_time, mem, p.returncode)



def get_params(args):
    for N in args.traces_nums:
        for B in args.nbytes:
            for _ in range(0, args.trials):
                yield N, B, args

def run(args):
    print(f"\033[1;34mRunning using {args.j or 'automatic # of'} workers, output file is {args.out}\n\033[0m", file=stderr)
    print("Traces numbers: ", args.traces_nums)
    print("Bytes: ", args.nbytes)
    print("Run each configuration", args.trials, "times")

    verbose = args.verbose

    N = len(args.traces_nums) * len(args.nbytes) * args.trials
    n = 0

    print("Altogether,", N, "runs get executed\n")

    with Pool(processes=args.j) as pool,\
         open(args.out, "w") as out:
        for rows in pool.imap_unordered(run_one, get_params(args)):
            for row in rows:
                print(*row, file=out)

                progress = 100 * (n / N)
                if verbose:
                    print(f"{progress: .2f}%: ", *row)
                else:
                    print(f"\r\033[32;1mDone: {progress: .2f}%\033[0m", end="")

                n += 1

        print("\nAll done!")
        print("Results stored into", args.out)


def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", metavar="PROC_NUM", action='store', type=int)
    parser.add_argument("--out", help="Name of the output file. Default is 'out.csv'", action='store', default="out.csv")
    parser.add_argument("--verbose", help="Print some extra messages", action='store_true', default=False)
    #parser.add_argument("--traces-dir", help="Take traces from this dir. If the dir does not exists, generate traces to this dir", action='store')

    parser.add_argument("--monitors", help="Comma-separated list of monitors: shl,ehl (default: shl,ehl)", action='store',
                        default="shl,ehl")

    parser.add_argument("--traces-nums", help="Comma-separated list of numbers of traces", action='store',
                        default=[500, 1000, 1500])
    parser.add_argument("--nbytes", help="Comma-separated list of nbytes for the alphabet. Currently only 16.",
                        action='store', default=[16])
    parser.add_argument("--trials", help="How many times repeat each run", action='store', type=int, default=10)
    parser.add_argument("--timeout", help="In seconds", action='store', type=int, default=120)

    args = parser.parse_args()

    if isinstance(args.traces_nums, str):
        args.traces_nums = list(map(int, args.traces_nums.split(",")))
    if isinstance(args.nbytes, str):
        args.nbytes = list(map(int, args.nbytes.split(",")))

    for b in args.nbytes:
        if b not in (4, 8, 16):
            raise RuntimeError("Invalid bytes given")
    for n in args.traces_nums:
        if n not in (500, 1000, 1500, 2000):
            raise RuntimeError("Invalid number of traces given")

    args.monitors = args.monitors.split(',')

    return args

if __name__ == "__main__":
    args = parse_cmd()
    run(args)
