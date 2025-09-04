# Building the artifact

## Building docker image


## Building without docker

### Structure of the artifact

```
- hna        sHL monitors
- hna-ifm24  eHL monitors
- mpt        MPT monitors
- rvhyper    RVHyper
- experiments   # Experiments with observational determinism
```

### Building without docker

The best would be to follow the steps from `Dockerfile`.
Here are the main steps that you need to do.

Setup python virtual environment

```shell
python3 -m venv venv/
```

Then, in every terminal where you will be working with this artifact,
run this command:

```shell
source venv/bin/activate
```

Bootstrap the `hna` project -- this is the project that generates the monitors.

```shell
# skip this command if you have run it in this terminal already
source venv/bin/activate

# get the hna project
git submodule update --init
cd hna

# install dependencies
pip3 install -r requirements

# configure the hna project
cmake . -DCMAKE_BUILD_TYPE=Release
```

For generating plots, you need also:
```
pip install matplotlib pandas seaborn
apt-get install texlive-latex-base texlive-latex-extra
```

NOTE: installing latex downloads a lot of data. You may skip this step
and the plotting scripts will automatically avoid using Latex.


## Building monitors

## eHL and sHL monitors

These monitors are built automatically by scripts.
If you want to build them manually, check the README.md in each
particular experiments.

### Source code for generating sHL monitors

The directory `hna` contains the code for generating sHL monitors.
Check the README in that directory for usage.
For doing new experiments, check the paragraph about RVHyper below.

### Source code for generating eHL monitors

The directory `hna-ifm24` contains code of the `hna` project that was used to run experiments for the paper "Monitoring Extended Hypernode Logic" presented at iFM'24.
We made the following changes to the code:

- The generated code is not formatted with `clang-format`. Formatting the generated code may take a lot of time and it would introduce bias into measurements of the time of code generation.

For doing new experiments, check the paragraph about RVHyper below.

## MPTs monitors

The source code is copied from the artifact of the paper *Monitoring Hyperproperties With Prefix Transducers*
that has been accepted at RV'23. This source code is available at <https://github.com/ista-vamos/rv23-experiments>.
We have done small changes to minimize the necessary code and made it compatible with our experiments.
In particular, we used only the monitor that can read inputs in the RVHyper format (eHL monitors can read this format too).
We removed all the other monitors.

To re-compile the monitor, use the commands:

```
cmake . -Dvamos_DIR=$(pwd)/../hna/vamos -DCMAKE_BUILD_TYPE=Release
make -j2
```

## RVHyper

The source code is a clone of the official repository at <https://github.com/reactive-systems/rvhyper>.
We have done the following changes, the first one to be able to compile RVHyper, the rest to increase the fairness of the comparison:

- We switched to C++17 standard which was necessary for a successful compilation as the code uses
   some C++ 17 features.
- We added the ability to look for all possible violations of the given property, so that the monitor
   does not stop after hitting the first error (other monitors also work this way).
- We do not print every processed event if `-q` is specified on the command line. This is to avoid the overhead of printing (other monitors also do not print the events).
- We do not build RVHyper with EAHyper, because EAHyper did not seem to work correctly in our tests (it was not able to decide the symmetry of simple formulas).
   Instead, we hard-coded that the input formula is reflexive and symmetric. Other monitors also work with the reflexivity and symmetry assumption without any computation on the formula.

All the changes that we have done are summarized in the patch `rvhyper.patch` in this directory.

To re-compile this monitor, use the commands:

```
# Download and compile SPOT (skip if already done)
curl -LRO https://www.lrde.epita.fr/dload/spot/spot-2.8.7.tar.gz
tar xf spot-2.8.7.tar.gz
cd /opt/artifact/monitors/rvhyper/spot-2.8.7
./configure --enable-c++17 --disable-python --disable-debug && make -j2 && make install

cd /opt/artifact/monitors/rvhyper
# you can change the makefile to use gcc and skip the next command
apt-get install -y --no-install-recommends clang

make -j2
```

## RVHyper

TBD
