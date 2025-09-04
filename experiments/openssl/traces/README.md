# Traces for experiments with OpenSSL

There are these directories:
 - `data`        Raw data obtained from OpenSSL
 - `traces-64b`  Traces obtained from data that use 64-bit integers
 - `traces-8b`   Traces obtained from data where 64-bit integers were broken
                 down to 8-bit integers (for eHL monitors -- not used in the paper).

## Generating traces

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


### Pre-processing the traces

The traces need to be put into the format that monitors can read.
This was done by the following command:

```
for I in `seq 1 24040`; do ./gentr.py 1 data/test-$I-in.txt data/test-$I-out.txt > test-$I.tr; done
```



