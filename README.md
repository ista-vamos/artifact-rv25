# Artifact for *Monitoring Hypernode Logic Over Infinite Domains*

The artifact was created to the paper *Monitoring Hypernode Logic Over Infinite Domains*
accepted at
[25th International Conference on Runtime Verification (RV'25)](https://rv25.isec.tugraz.at/).

## Setting up the docker image

TBD

## Running

For short version of the experiments, run `make short`. These experiments take a few minutes.
For full experiments, run `make full`. These experiments take XXX.


## Structure of the artifact

```
- experiments   # Experiments with observational determinism
- hna           # sHL monitors
- hna-ifm24     # eHL monitors
- mpt           # MPT monitors
- rvhyper       # RVHyper
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


## Building

See `BUILDING.md`.

