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

### Building OpenSSL with fuzzing

```
CC=clang ./config enable-fuzz-libfuzzer \
        -DPEDANTIC  no-shared \ 
        --with-fuzzer-lib=/usr/lib/clang/19/lib/linux/libclang_rt.fuzzer-x86_64.a\
        -DFUZZING_BUILD_MODE_UNSAFE_FOR_PRODUCTION \
        -fsanitize=fuzzer-no-link \
        enable-ec_nistp_64_gcc_128 -fno-sanitize=alignment \
        enable-weak-ssl-ciphers enable-rc5 enable-md2 \
        enable-ssl3 enable-ssl3-method enable-nextprotoneg \
        --debug

LDCMD=clang++ make -j4
```

## Structure of the artifact

```
- ifm24   # Experiments from the paper "Monitoring Extended Hypernode Logic" from iFM 2024
```
