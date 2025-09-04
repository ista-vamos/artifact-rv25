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
hnl_dir = join(bindir, ".")


def errlog(*args):
    with open(join(dirname(__file__), "log.txt"), "a") as logf:
        for a in args:
            print(a, file=logf)

def run_one(arg):
    traces_num, monitors, bits, args = arg
    traces_dir = args.traces_dir
    if traces_dir is None:
        traces_dir = join(bindir, f'traces/traces-{bits}b')

    # get the list of files
    files = [fl for fl in listdir(traces_dir) if fl.endswith(".tr")][:traces_num]

    results = []

    if "ehl" in monitors:
        results.append(run_hnl(arg, traces_dir, files, "ehl"))
    if "shl-eq" in monitors:
        results.append(run_hnl(arg, traces_dir, files, "shl-eq"))

    return results


def run_hnl(arg, traces_dir, files, ty):
    traces_num, trace_len, bits, args = arg
    if ty.startswith("ehl"):
        mon = f'{ty}-{bits}b'
    else:
        assert ty.startswith("shl"), ty
        mon = ty
    cmd = ["/bin/time", "-f", '%Uuser %Ssystem %eelapsed %PCPU (%Xavgtext+%Davgdata %Mmaxresident)k',
           join(f"{hnl_dir}/{mon}", "monitor")]
    cmd += files
    p = Popen(cmd, stderr=PIPE, stdout=PIPE, cwd=traces_dir, preexec_fn=os.setsid)
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

    return (f"{ty}", traces_dir, traces_num, trace_len, bits, verdict, instances, atoms, reused_mons, reused_verdicts, cpu_time, wall_time, mem, p.returncode)


mon2bits = {
        'shl-eq' : 64,
        'ehl' : 8,
}

def get_params(args):
    for N in args.traces_nums:
        for M in args.monitors:
            for _ in range(0, args.trials):
                yield N, [M], mon2bits[M], args

def run(args):
    print(f"\033[1;34mRunning using {args.j or 'automatic # of'} workers, output file is {args.out}\n\033[0m", file=stderr)
    print("Traces numbers: ", args.traces_nums)
    print("Run each configuration", args.trials, "times")

    verbose = args.verbose

    N = len(args.monitors) * len(args.traces_nums) * args.trials
    n = 0

    print("Altogether,", N, "runs get executed\n")
    print("-------------------------------------")

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
    parser.add_argument("--traces-dir", help="Take traces from this dir.", action='store')

    parser.add_argument("--traces-nums", help="Comma-separated list of numbers of traces", action='store',
                        default=[1000, 5000, 10000, 15000, 20000])
    parser.add_argument("--trials", help="How many times repeat each run", action='store', type=int, default=10)
    parser.add_argument("--timeout", help="In seconds", action='store', type=int, default=300)
    parser.add_argument("--monitors", help="List of monitors: shl-eq", action='store',
                        default="shl-eq")

    parser.add_argument("--traces-no-stuttering", help="Generate traces with no stuttering", action='store_true', default=False)

    args = parser.parse_args()

    if args.traces_dir:
        args.traces_dir = abspath(args.traces_dir)
    if isinstance(args.traces_nums, str):
        args.traces_nums = list(map(int, args.traces_nums.split(",")))

    args.monitors = args.monitors.split(",")

    return args

if __name__ == "__main__":
    args = parse_cmd()
    run(args)


def shl_monitors(args):
    for m in args.monitors:
        if m.startswith("shl"):
            yield m

if __name__ == "__main__":
    args = parse_cmd()

    problem=False
    for mon in shl_monitors(args):
        mon = join(f"{hnl_dir}/{mon}", "monitor")
        if not (isfile(mon) and access(mon, X_OK)):
            print(f"Did not find sHL monitor ({mon}). Please run `'./generate-shl.sh` "
                   "first (you may need to modify the script to generate the right monitor).",
                  file=stderr)
            problem=True

    if problem:
        exit(1)

    # do it!
    run(args)
