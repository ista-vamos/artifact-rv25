# RV'25 changes

## Transforming traces

```
for F in traces-16-if24/traces-500/*.tr; do python3 transform_trace.py $F > traces-16/traces-500/$(basename $F); done
```

---------------------------------------------------
The folder `libhydrogen` contains the source code of libhydrogen that can be
used to generate the traces. Pre-generated traces that we used for our
experiments are in folders `traces-X`, where X is the number of input bytes
used while generating the traces.

## Re-generating the traces

The artifact does not include this step to keep a smaller size.
For generating the traces anew, you need VAMOS compiled with `LLVM_SOURCES=ON`.
Clone VAMOS (<https://github.com/ista-vamos/vamos>) and build it following the
instructions in its README. Make sure that `LLVM_SOURCES=ON` (it should be the
default).

Then, install `wllvm` script through pip:

```
pip install wllvm
```

Now you can generate LLVM bitcode for _libhydrogen_:

```
make -f Makefile.libhydrogen
```

The last step should produce `libhydrogen.bca`.
Then, modify the path to VAMOS sources in the script `hash.sh` and run it.
It should generate multiple binaries that execute the code from `libhydrogen_hash.c`
which is instrumented to generate traces that can be monitored.

Finally, run `gen-traces.sh` to generate the traces (see the help message of the script):

```
for B in 4 8 16; do
  for N in 500 1000 1500; do
    ./gen-traces.sh $B $N ../traces-$B/traces-$N <path-to-hnl.py>
  done
done
```

## Generating the monitors

_After_ generating the traces, you can generate the monitors using the `generate.sh` script.
It is important to generate traces first, because as a part of generating the traces,
the eHL formulas and CSV headers specification are also generated and are used for generating the monitors.
