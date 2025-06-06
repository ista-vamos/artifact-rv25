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
#mpt_binary = join(bindir, "mpts/monitor")
#rvhyper_dir = join(bindir, "rvhyper/")
hnl_dir = join(bindir, ".")

def errlog(*args):
    with open(join(dirname(__file__), "log.txt"), "a") as logf:
        for a in args:
            print(a, file=logf)

def run_one(arg):
    traces_num, trace_len, bits, args = arg
    traces_dir = mkdtemp(prefix="/tmp/")

    # -- GENERATE TRACES
    # print(f"  \033[37;1m.. [{datetime.datetime.now().time()}] running # traces = {traces_num}, len = {trace_len}, bits = {bits}\033[0m", file=stderr)
    #stderr.flush()

    trnum = 1 if args.one_trace else traces_num
    opts='force-od'
    if args.traces_no_stuttering:
        opts += ",no-stuttering"
    runcmd(["python3", f"{bindir}/gen-traces.py",
            str(trnum), str(trace_len), str(bits), f"{opts},outdir={traces_dir}"],
            stderr=DEVNULL,
            stdout=DEVNULL, check=True)

    # get the list of files
    if args.one_trace:
        files = ["1.tr"] * traces_num
    else:
        files = [fl for fl in listdir(traces_dir) if fl.endswith(".tr")]

    results = []

    monitors = args.monitors

    if "mpt" in monitors:
        results.append(run_mpt(arg, traces_dir, files))
    if "rvhyper" in monitors:
        results.append(run_rvhyper(arg, traces_dir, files))
    if "ehl" in monitors:
        results.append(run_hnl(arg, traces_dir, files, "ehl"))
    if "ehl-stred" in monitors:
        results.append(run_hnl(arg, traces_dir, files, "ehl-stred"))
    if "shl-le" in monitors:
        results.append(run_hnl(arg, traces_dir, files, "shl-le"))
    if "shl-eq" in monitors:
        results.append(run_hnl(arg, traces_dir, files, "shl-eq"))
    if "shl-le-stred" in monitors:
        results.append(run_hnl(arg, traces_dir, files, "shl-le-stred"))
    if "shl-eq-stred" in monitors:
        results.append(run_hnl(arg, traces_dir, files, "shl-eq-stred"))

    try:
        rmtree(traces_dir)
    except Exception as e:
        print("Failed removing traces: ", e, file=stderr)
        rmtree(traces_dir, ignore_errors=True)

    return results


def run_rvhyper(arg, traces_dir, files, rvh_args=None):
    traces_num, trace_len, bits, args = arg
    rvh = join(rvhyper_dir, "build/release/rvhyper")
    assert access(rvh, X_OK), f"Cannon find rvhyper binary, assumed is {rvh}"
    cmd = ["/bin/time", "-f", '%Uuser %Ssystem %eelapsed %PCPU (%Xavgtext+%Davgdata %Mmaxresident)k', rvh]
    if rvh_args:
        cmd += rvh_args
    cmd += ["-S", f"{traces_dir}/od-{bits}b.hltl"] + files
    # print("> ", " ".join(cmd))

    p = Popen(cmd, stderr=PIPE, stdout=PIPE, cwd=traces_dir, preexec_fn=os.setsid)
    try:
        out, err = p.communicate(timeout=args.timeout)
        if p.returncode != 0:
            errlog(env, p, out, err)
    except TimeoutExpired:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM)
        out, err = p.communicate(timeout=10)

    assert err is not None, cmd

    cpu_time=None
    wall_time=None
    mem=None

    if p.returncode == 0:
        for line in err.splitlines():
            if b"elapsed" in line:
                parts = line.split()
                assert b"user" in parts[0]
                assert b"elapsed" in parts[2]
                assert b"maxresident" in parts[5]

                try:
                    cpu_time = float(parts[0][:-4])
                    wall_time = float(parts[2][:-7])
                    mem = int(parts[5][:-13])/1024.0
                except ValueError as e:
                    print(err, file=sys.stderr)
                    raise e
    else:
        errlog("Faield running RVHyper:", out, err)


    return (f"rvhyper", traces_dir, traces_num, trace_len, bits, cpu_time, wall_time, mem, p.returncode)



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

def run_mpt(arg, traces_dir, files):
    traces_num, trace_len, bits, args = arg
    cmd = ["/bin/time", "-f", '%Uuser %Ssystem %eelapsed %PCPU (%Xavgtext+%Davgdata %Mmaxresident)k',
           mpt_binary]
    cmd += files
    p = Popen(cmd, stderr=PIPE, stdout=PIPE, cwd=traces_dir, preexec_fn=os.setsid)
    try:
        out, err = p.communicate(timeout=args.timeout)
    except TimeoutExpired:
        os.killpg(os.getpgid(p.pid), signal.SIGTERM) 
        out, err = p.communicate(timeout=10)
    assert err is not None, cmd


    # Max workbag size: 7391
    #Traces #: 500
    #1.73user 0.03system 0:01.76elapsed 99%CPU (0avgtext+0avgdata 137604maxresident)k
    #0inputs+0outputs (0major+34642minor)pagefaults 0swaps
    wbg_size=None
    cpu_time=None
    wall_time=None
    mem=None
    if p.returncode in (0, 1):
        for line in out.splitlines():
            line = line.strip()
            if line.startswith(b"Max workbag"):
                wbg_size = int(line.split()[3])

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
        errlog("Faield running MPT monitor:", out, err)

    return ("mpt", traces_dir, traces_num, trace_len, bits, wbg_size, cpu_time, wall_time, mem, p.returncode)


def get_params(args):
    for N in args.traces_nums:
        for L in args.traces_lens:
            for B in args.bits:
                for _ in range(0, args.trials):
                    yield N, L, B, args

def run(args):
    print(f"\033[1;34mRunning using {args.j or 'automatic # of'} workers, output file is {args.out}\n\033[0m", file=stderr)
    print("Traces lenghts: ", args.traces_lens)
    print("Traces numbers: ", args.traces_nums)
    print("Bits: ", args.bits)
    print("Run each configuration", args.trials, "times")
    if args.one_trace:
        print("All traces are the same one trace")

    verbose = args.verbose

    N = len(args.monitors) * len(args.traces_nums) * len(args.traces_lens) * len(args.bits) * args.trials
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
    #parser.add_argument("--traces-dir", help="Take traces from this dir. If the dir does not exists, generate traces to this dir", action='store')

    parser.add_argument("--traces-lens", help="Comma-separated list of lenghts of traces", action='store',
                        default=[1000, 2000, 3000])
    parser.add_argument("--traces-nums", help="Comma-separated list of numbers of traces", action='store',
                        default=[1000, 2000, 3000, 4000, 5000])
    parser.add_argument("--bits", help="Comma-separated list of bits for the alphabet (not affecting mpt and shl monitors). Supported are any combination of 1, 2, 4, 8, 10.",
                        action='store', default=[2,4,8])
    parser.add_argument("--trials", help="How many times repeat each run", action='store', type=int, default=10)
    parser.add_argument("--timeout", help="In seconds", action='store', type=int, default=120)
    parser.add_argument("--monitors", help="List of monitors: mpt, rvhyper, ehl, eh-stred,shl-le,shl-eq,shl-le-stred,shl-eq-stred", action='store',
                        #default="mpt,rvhyper,hnl")
                        default="ehl,ehl-stred,shl-le,shl-eq,shl-le-stred,shl-eq-stred")

    parser.add_argument("--one-trace", help="Make all traces same", action='store_true', default=False)
    parser.add_argument("--traces-no-stuttering", help="Generate traces with no stuttering", action='store_true', default=False)

    args = parser.parse_args()

    #if args.traces_dir:
    #    args.traces_dir = abspath(args.traces_dir)
    if isinstance(args.traces_lens, str):
        args.traces_lens = list(map(int, args.traces_lens.split(",")))
    if isinstance(args.traces_nums, str):
        args.traces_nums = list(map(int, args.traces_nums.split(",")))
    if isinstance(args.bits, str):
        args.bits = list(map(int, args.bits.split(",")))

    args.monitors = args.monitors.split(",")

    return args

if __name__ == "__main__":
    args = parse_cmd()
    run(args)
