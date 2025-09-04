# Artifact for *Monitoring Hypernode Logic Over Infinite Domains*

The artifact was created to the paper *Monitoring Hypernode Logic Over Infinite Domains*
accepted at
[25th International Conference on Runtime Verification (RV'25)](https://rv25.isec.tugraz.at/).

The artifact can automatically reproduce the experiments with running monitors,
in particular:
 - Fig. 7 (`experiments/ehl-shl` and `experiments/ifm24`),
 - Table 1 (`experiments/openssl`)

The artifact does not have scripts to automatically reproduce the experiments presented
in Fig. 8. that measure the time of generating monitors.
You can, however, reproduce them manually -- the artifact contains code for generating the monitors
and you can run it and measure the time (how to do this is described later).
There is also the script we used to generate Fig. 8 (`plots/gentime.py`).

When the artifact is set-up (see below), go into the top-level directory and run one of
 - `make short`
 - `make full`

To run experiments and generate plots.
The command `make short` runs a short version of the experiments and it takes a few minutes.
Full experiments are ran with `make full`. These experiments take XXX.

## Building

We recommend build the artifact using Docker (Podman).
In case you want to build the artifact from scratch, see `BUILDING.md`.


## Setting up the Docker image

TBD


## Structure of the artifact

```
- experiments   # Experiments with observational determinism
- hna           # sHL monitors
- hna-ifm24     # eHL monitors
- mpt           # MPT monitors
- rvhyper       # RVHyper (HyperLTL monitors)
```

### eHL and sHL monitors

XXX: hna vs hna-ifm24
XXX: RVHyno

### MPT monitors

MPT monitors were taken from XXX.
We modified them to read events in the RVHyper format, as that is the format of traces
we use in the experiments with MPTs.

### RVHyper monitors

XXX: Origin and Modifications



