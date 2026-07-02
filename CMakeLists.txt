cmake_minimum_required(VERSION 3.20)

project(interactive_data_structures_simulator LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)

execute_process(
    COMMAND "${Python_EXECUTABLE}" -m pybind11 --cmakedir
    OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
    RESULT_VARIABLE PYBIND11_DISCOVERY_RESULT
)

if(NOT PYBIND11_DISCOVERY_RESULT EQUAL 0)
    message(FATAL_ERROR "Pybind11 nao foi encontrado. Execute: python -m pip install pybind11")
endif()

list(PREPEND CMAKE_PREFIX_PATH "${PYBIND11_CMAKE_DIR}")
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(ds_core
    cpp/src/bindings.cpp
    cpp/src/data_structures.cpp
)

target_include_directories(ds_core PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/cpp/include")

target_compile_options(ds_core PRIVATE
    $<$<CXX_COMPILER_ID:GNU,Clang>:-Wall -Wextra -Wpedantic>
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
)

set_target_properties(ds_core PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}"
)
