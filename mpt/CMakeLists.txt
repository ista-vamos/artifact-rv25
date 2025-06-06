cmake_minimum_required(VERSION 3.10)
project(MPTs)

set(CMAKE_VERBOSE_MAKEFILE 1)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if (vamos_DIR)
  set(vamos-buffers_DIR ${vamos_DIR}/vamos-buffers/cmake/vamos-buffers)
  set(vamos-common_DIR ${vamos_DIR}/vamos-common/cmake/vamos-common)
  set(vamos-sources_DIR ${vamos_DIR}/vamos-sources/cmake/vamos-sources)
endif()

find_package(vamos-buffers REQUIRED)
include_directories(${vamos_buffers_INCLUDE_DIRS})

add_subdirectory(src)

# monitor that reads the inputs in the same format as rvhyper
add_executable(monitor src/main_argv.cpp inputs/rvhyper.cpp)
target_include_directories(monitor PUBLIC ${vamos-buffers_INCLUDE_DIRS}
       PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/
       PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/..)
target_link_libraries(monitor PRIVATE monitor-od)

