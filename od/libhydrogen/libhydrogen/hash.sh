#!/bin/bash
#

set -e
set -x


cd $(dirname $0)
LIBHYDROGEN_BCA=libhydrogen.bca
vamos_sources_SRCDIR=/opt/vamos/hna/vamos/vamos-sources

llvm-link libhydrogen.bca -o libhydrogen.bc

clang -g libhydrogen_hash.c -c -emit-llvm -I $(pwd)/libhydrogen $CFLAGS
llvm-link libhydrogen.bc libhydrogen_hash.bc -o hydrogen_hash.bc
opt hydrogen_hash.bc -O2 -o hydrogen_hash-opt.bc

opt -tbaa -basic-aa --bugpoint-enable-legacy-pm\
       -load ${vamos_sources_SRCDIR}/src/llvm/store-load/store-load-instrumentation.so\
       -vamos-store-load-instr hydrogen_hash.bc -o hydrogen_hash-instr.bc

opt -tbaa -basic-aa --bugpoint-enable-legacy-pm\
	-load ${vamos_sources_SRCDIR}/src/llvm/store-load/store-load-instrumentation.so\
	-vamos-store-load-instr hydrogen_hash-opt.bc -o hydrogen_hash-opt-instr.bc

opt -tbaa -basic-aa --bugpoint-enable-legacy-pm\
       -load ${vamos_sources_SRCDIR}/src/llvm/store-load/store-load-instrumentation.so\
       -vamos-store-load-instr -vamos-store-load-stepping hydrogen_hash.bc -o hydrogen_hash-instr-stepping.bc

opt -tbaa -basic-aa --bugpoint-enable-legacy-pm\
	-load ${vamos_sources_SRCDIR}/src/llvm/store-load/store-load-instrumentation.so\
	-vamos-store-load-instr  -vamos-store-load-stepping  hydrogen_hash-opt.bc -o hydrogen_hash-opt-instr-stepping.bc


clang -g hydrogen_hash-instr.bc -o hydro_hash ${vamos_sources_SRCDIR}/src/llvm/store-load/impl/libstore-load-impl-csv.a
clang -g hydrogen_hash-opt-instr.bc -o hydro_hash-opt ${vamos_sources_SRCDIR}/src/llvm/store-load/impl/libstore-load-impl-csv.a
clang -g hydrogen_hash-instr-stepping.bc -o hydro_hash-stepping ${vamos_sources_SRCDIR}/src/llvm/store-load/impl/libstore-load-impl-csv.a
clang -g hydrogen_hash-opt-instr-stepping.bc -o hydro_hash-opt-stepping ${vamos_sources_SRCDIR}/src/llvm/store-load/impl/libstore-load-impl-csv.a

