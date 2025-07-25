#target_compile_options(test2 PRIVATE -fsanitize=address,undefined)

if (vamos_DIR)
	message(STATUS "vamos_DIR given, assuming buffers and etc. are in the standard paths given by sub-modules")

	set(vamos-buffers_DIR ${vamos_DIR}/vamos-buffers/cmake/vamos-buffers)
	set(vamos-sources_DIR ${vamos_DIR}/vamos-sources/cmake/vamos-sources)
endif()

find_package(vamos-buffers REQUIRED)
find_package(vamos-sources REQUIRED)

get_filename_component(vamos-sources_SRCDIR ${vamos-sources_DIR}/../.. ABSOLUTE)

include_directories(${vamos-buffers_INCLUDE_DIRS})

get_target_property(vamos-buffers_vamos-buffers-lib vamos-buffers-lib LOCATION)
get_target_property(vamos-buffers_vamos-buffers-ringbuf vamos-buffers-ringbuf LOCATION)
get_target_property(vamos-buffers_vamos-buffers-shmbuf vamos-buffers-shmbuf LOCATION)
get_target_property(vamos-buffers_vamos-buffers-streams vamos-buffers-streams LOCATION)
get_filename_component(vamos-buffers_LIBRARIES_DIRS_lib ${vamos-buffers_vamos-buffers-lib} DIRECTORY)
get_filename_component(vamos-buffers_LIBRARIES_DIRS_core ${vamos-buffers_vamos-buffers-ringbuf} DIRECTORY)
get_filename_component(vamos-buffers_LIBRARIES_DIRS_shmbuf ${vamos-buffers_vamos-buffers-shmbuf} DIRECTORY)
get_filename_component(vamos-buffers_LIBRARIES_DIRS_streams ${vamos-buffers_vamos-buffers-streams} DIRECTORY)


add_executable(preprocess preproc.c)
target_link_libraries(preprocess vamos-buffers-lib
                                 vamos-buffers-stream
                                 vamos-buffers-streams
                                 vamos-buffers-shmbuf
                                 vamos-buffers-arbiter
                                 vamos-buffers-parallel-queue)

if (NOT EXISTS libhydrogen/CMakeLists.txt)
        file(ARCHIVE_EXTRACT INPUT ${CMAKE_SOURCE_DIR}/cryptomk-dataset/dataset/src/libhydrogen.tar.gz)
endif()

add_custom_command(OUTPUT libhydrogen.bca
                   COMMAND make -f Makefile.libhydrogen)

#################################
## libhydrogen_enc
#################################
add_custom_target(libhydrogen_enc.bc
                  COMMAND clang libhydrogen_enc.c -c -emit-llvm -I${CMAKE_CURRENT_SOURCE_DIR}/libhydrogen ${CMAKE_C_FLAGS}
                  DEPENDS libhydrogen.bca)

add_custom_target(hydrogen_enc.bc
                  COMMAND llvm-link libhydrogen.bca libhydrogen_enc.bc -o hydrogen_enc.bc
                  DEPENDS libhydrogen.bca libhydrogen_enc.bc)

add_custom_target(hydrogen_enc-instrumented.bc
		  #COMMAND opt -tbaa -basic-aa -enable-new-pm=false
                   COMMAND opt -tbaa -basic-aa --bugpoint-enable-legacy-pm
                               -load ${vamos-sources_SRCDIR}/src/llvm/store-load/store-load-instrumentation.so
                               -vamos-store-load-instr hydrogen_enc.bc -o hydrogen_enc-instrumented.bc
                   DEPENDS hydrogen_enc.bc)

add_custom_target(hydro_enc.o
                  COMMAND clang -c hydrogen_enc-instrumented.bc -o hydro_enc.o
                  DEPENDS hydrogen_enc-instrumented.bc) 

add_executable(hydro_enc hydro_enc.o)

set_target_properties(hydro_enc PROPERTIES LINKER_LANGUAGE C)
target_link_libraries(hydro_enc  ${vamos-sources_SRCDIR}/src/llvm/store-load/impl/libstore-load-impl.a)
target_link_libraries(hydro_enc vamos-buffers-lib
                            vamos-buffers-shmbuf
                            vamos-buffers-stream
                            vamos-buffers-streams
                            vamos-buffers-shmbuf
                            vamos-buffers-arbiter
			    vamos-buffers-parallel-queue)

 
add_executable(hydro_enc-csv hydro_enc.o)

set_target_properties(hydro_enc-csv PROPERTIES LINKER_LANGUAGE C)
target_link_libraries(hydro_enc-csv  ${vamos-sources_SRCDIR}/src/llvm/store-load/impl/libstore-load-impl-csv.a)


#################################
## libhydrogen_hash
#################################
add_custom_command(OUTPUT libhydrogen_hash.bc
                   COMMAND clang libhydrogen_hash.c -c -emit-llvm -I${CMAKE_CURRENT_SOURCE_DIR}/libhydrogen ${CMAKE_C_FLAGS}
                   DEPENDS libhydrogen.bca)

add_custom_command(OUTPUT hydrogen_hash.bc
                   COMMAND llvm-link libhydrogen.bca libhydrogen_hash.bc -o hydrogen_hash.bc
                   DEPENDS libhydrogen.bca libhydrogen_hash.bc)

add_custom_command(OUTPUT hydrogen_hash-instrumented.bc
		  #COMMAND opt -tbaa -basic-aa -enable-new-pm=false
                   COMMAND opt -tbaa -basic-aa --bugpoint-enable-legacy-pm
                               -load ${vamos-sources_SRCDIR}/src/llvm/store-load/store-load-instrumentation.so
                               -vamos-store-load-instr hydrogen_hash.bc -o hydrogen_hash-instrumented.bc
                   DEPENDS hydrogen_hash.bc)

add_custom_command(OUTPUT hydro_hash.o
                   COMMAND clang -c hydrogen_hash-instrumented.bc -o hydro_hash.o
                   DEPENDS hydrogen_hash-instrumented.bc) 

add_executable(hydro_hash hydro_hash.o)

set_target_properties(hydro_hash PROPERTIES LINKER_LANGUAGE C)
target_link_libraries(hydro_hash  ${vamos-sources_SRCDIR}/src/llvm/store-load/impl/libstore-load-impl.a)
target_link_libraries(hydro_hash vamos-buffers-lib
                            vamos-buffers-shmbuf
                            vamos-buffers-stream
                            vamos-buffers-streams
                            vamos-buffers-shmbuf
                            vamos-buffers-arbiter
			    vamos-buffers-parallel-queue)

 
add_executable(hydro_hash-csv hydro_hash.o)

set_target_properties(hydro_hash-csv PROPERTIES LINKER_LANGUAGE C)
target_link_libraries(hydro_hash-csv  ${vamos-sources_SRCDIR}/src/llvm/store-load/impl/libstore-load-impl-csv.a)

