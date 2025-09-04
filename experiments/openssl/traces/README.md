# Traces for experiments with OpenSSL

There are these directories:
 - `data`        Raw data obtained from OpenSSL
 - `traces-64b`  Traces obtained from data that use 64-bit integers
 - `traces-8b`   Traces obtained from data where 64-bit integers were broken
                 down to 8-bit integers (for eHL monitors -- not used in the paper).

## Generating traces

### Building OpenSSL

First, clone OpenSSL sources. For our experiments, we used the commit `a0d1af6574ae6a0e3`.
Then, apply the patch `client.patch` that makes the `fuzz/client` binary
print events into files.  Then, build OpenSSL with fuzzing:

```sh
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

### Running fuzzing

Run the fuzzing tests with `fuzz/client` (see OpenSSL's docs for details).
This step will generate a bunch of raw traces in files `test-<NUM>-in.txt`
and `test-<NUM>-out.txt`.
These raw traces need to be put into the format that monitors can read.
This was done by these commands:

```sh
# traces were generated into the directory `data`
RAW_TRACES_DIR=data
BITS=64
mkdir traces-${BITS}

for I in `seq 1 $(ls $RAW_TRACES_DIR/*-in.txt | wc -l)`; do
  ./gentr.py ${BITS} $RAW_TRACES_DIR/test-$I-in.txt $RAW_TRACES_DIR/test-$I-out.txt > traces-${BITS}b/test-$I.tr;
done
```

