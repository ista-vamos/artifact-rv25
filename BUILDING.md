# Building the artifact

If you have not done so yet, clone the repository.

```sh
git clone https://github.com/ista-vamos/artifact-rv25
cd artifact-rv25
```

Unless stated otherwise, we assume that all commands described
subsequently are executed from the `artifact-rv25` directory.


## Building docker image

The top-level directory of the artifact contains `Dockerfile`,
so simply run:

```sh
build . -t rv25-shl
```


## Building without docker

The best is to follow the steps from `Dockerfile`.
The guide below explains and elaborates on of those steps.


### Python virtual environment

First, if outside docker, you may need to setup python virtual environment:

```sh
python3 -m venv venv/
```

Then, in every terminal where you will be working with this artifact,
run this command:

```sh
source venv/bin/activate
```

### Building HNA

Bootstrap the `hna` project -- this is the project that generates the monitors.

```sh
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


### Building HNA from iFM'24

eHL monitors are build using an older version of HNA.
It was checked out together with the `hna` directory,
but we need to configure it:

```sh
cd hna-ifm24
cmake . -DCMAKE_BUILD_TYPE=Release -Dvamos_DIR=$(pwd)/../hna/vamos
```

### MPTs monitors

To compile the MPT monitor, use the commands:

```sh
cd mpt
cmake . -Dvamos_DIR=$(pwd)/../hna/vamos -DCMAKE_BUILD_TYPE=Release
make -j2
```

## RVHyper

To compile RVHyper, you must first build SPOT (unless your system has the right version
of SPOT installed. You may try and will see if the build fails).

```sh
cd rvhyper

# Download and compile SPOT (skip if already done)
curl -LRO https://www.lrde.epita.fr/dload/spot/spot-2.8.7.tar.gz
tar xf spot-2.8.7.tar.gz
cd spot-2.8.7
./configure --enable-c++17 --disable-python --disable-debug --prefix=$(pwd)/spot-install && make -j2 && make install

# export the path to `libspot.pc` and `libbddx.pc`
export PKG_CONFIG_PATH=$(pwd)/spot-install/lib/pkgconfig

# --- now you can build RVHyper ----
cd ..

# you can change the makefile to use gcc and skip the next command
apt-get install -y --no-install-recommends clang

make -j2
```

## Plots

For generating plots, you will need:

```sh
pip install matplotlib pandas seaborn
```

(You can use the system packages instead of using pip).
Optionally, you may also install latex if you do not already have it.
Labels in plots will then be typeset using Latex:

```sh
apt-get install texlive-latex-base texlive-latex-extra cm-super
```

NOTE: installing Latex downloads a lot of data. You may skip this step
and the plotting scripts will automatically avoid using Latex.
In the exported docker image, we do not use latex to keep the
image smaller. You can always run the command above when
creating a new docker container. (The command is also
in the Dockerfile, commented out).

