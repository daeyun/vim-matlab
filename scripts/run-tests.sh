#!/usr/bin/env bash

set -o xtrace

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
SRC_ROOT="${DIR}/../rplugin/python"

cd ${DIR}/..

PYTHONPATH="${SRC_ROOT}:${SRC_ROOT}/vim_matlab" py.test -s
