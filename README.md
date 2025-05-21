# Artifact for RV'25

## Building

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

# build VAMOS -- necessary to setup vamos-common subproject in VAMOS
./build-vamos.sh

# configure the hna project
cmake .
```
