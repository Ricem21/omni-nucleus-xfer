#!/bin/bash

set -e


export SCRIPT_DIR=/opt/omni-client/connect-samples-205.0.0 

export USD_LIB_DIR=${SCRIPT_DIR}/_build/linux-x86_64/release
export PYTHON=${SCRIPT_DIR}/_build/target-deps/python/python

export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${USD_LIB_DIR}
export PYTHONPATH=${USD_LIB_DIR}/python:${USD_LIB_DIR}/bindings-python

if [ ! -f ${PYTHON} ]; then
    echo "echo Python, USD, and Omniverse Client libraries are missing.  Run \"./repo.sh build --stage\" to retrieve them."
    popd
    exit
fi

${PYTHON} access-test.py "$@"

