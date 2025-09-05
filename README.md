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
and you can run it and measure the time (how to generate monitors is described later).
There is also the script we used to generate Fig. 8 (`plots/gentime.py`).

To run experiments and generate plots, setup the artifact (see below),
go into the top-level directory and run one of:

 - `make short`
 - `make full`

The command `make short` runs a short version of the experiments and it takes cca 5 minutes on a
recent hardware (as of 2025).
Full experiments are ran with `make full`. These experiments take tens of minutes to a small number
of hours, depending on the hardware.

## Setup

We recommend using this artifact from Docker (Podman).
In case you are using the exported image (built for x86),
first load the docker image:

```sh
docker load < rv25-shl.tar.gz
```

This is a one-time action and you do not need to repeat it in the future.
Then, start a new container using this command:

```

docker run --rm -ti -v "$(pwd)/results":/opt/artifact/results rv25-shl
```

When you are inside the container, you can run `make short` or `make full`.
The results will be exported into the directory `results` in the directory
from where you started docker.

NOTE: to keep the exported image smaller, we do not include latex packages
that may be used to typeset labels in the plots in the same way as they are
in the paper. If you want to use latex labels, after running the docker container,
run this command:

```sh
apt-get install texlive-latex-base texlive-latex-extra cm-super
```

Plots are generated automatically by `make short` and `make full` commands.
If you want to re-generate them manually, run `make -C plots`.
They are stored into the `results` directory inside the directory from where
you started docker image (or in the `artifact-rv25` if you are not using docker).

For more information about the experiments, see README.md files inside directories.
For building the artifact, either using docker or from scratch, see `BUILDING.md`.


## Structure of the artifact

```
- experiments   # Experiments with observational determinism
- hna           # code for generating sHL monitors
- hna-ifm24     # code for generating eHL monitors
- mpt           # code of the MPT monitors
- plots         # scripts for generating plots
- rvhyper       # RVHyper (HyperLTL monitors)
```

### Code of eHL and sHL monitors

The code for generating eHL and sHL monitors is a part of the
[RVHyno](https://github.com/ista-vamos/rvhyno) project, previously called HNA.
The code is in two directories:
 - `hna`        for sHL monitors
 - `hna-ifm24`  for eHL monitors

Directory `hna-ifm24` contains the project in the version used in the artifact
for the paper _Monitoring Extended Hypernode Logic_ that was accepted at iFM'24:
 - [artifact](https://doi.org/10.5281/zenodo.13294507)
 - [paper](https://doi.org/10.1007/978-3-031-76554-4_9)
We made the following changes to the code:

- The generated code is not formatted with `clang-format`. Formatting the generated
  code may take a lot of time and it would introduce bias into measurements of the time
  of code generation.

Directory `hna` contains the new code for generating sHL monitors.

Directories `hna` and `hna-ifm24` contain the script `hnl.py` that generates the monitors.
See README inside those directories for further usage.

### RVHyno

The current version of the project is available at
<https://github.com/ista-vamos/rvhyno>

it contains many improvements, so if you want to experiment with hypernode logic monitors,
we suggest you try the current version.
You can get it simply by cloning and configuring the repository:

```sh
git clone https://github.com/ista-vamos/rvhyno
cd rvhyno

# now follow the README
```

### MPT monitors

MPT monitors were taken from the artifact for _Monitoring Hyperproperties Using Prefix Transducers_
presented at RV'23:

 - [artifact](https://doi.org/10.5281/zenodo.8191722)
 - [paper](https://link.springer.com/chapter/10.1007/978-3-031-44267-4_9)

We modified the monitors to read events in the RVHyper format, as that is the format of traces
we use in the experiments with MPTs. We have also removed code unnecessary for this artifact.


### RVHyper

The source code of RVHyper is a clone of the official repository that can be found
at <https://github.com/reactive-systems/rvhyper>.
We have done the following changes, the first one to be able to compile RVHyper,
the rest to increase the fairness of the comparison:

- We switched to C++17 standard which was necessary for a successful compilation as the code uses
   some C++ 17 features.
- We added the ability to look for all possible violations of the given property, so that the monitor
   does not stop after hitting the first error (other monitors also work this way).
- We do not print every processed event if `-q` is specified on the command line. This is to avoid the overhead of printing (other monitors also do not print the events).
- We do not build RVHyper with EAHyper, because EAHyper did not seem to work correctly in our tests (it was not able to decide the symmetry of simple formulas).
   Instead, we hard-coded that the input formula is reflexive and symmetric. Other monitors also work with the reflexivity and symmetry assumption without any computation on the formula.

All the changes that we have done are summarized in the patch `rvhyper.patch` in the directory `rvhyper`.

