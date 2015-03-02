#!/bin/sh

set -o xtrace

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd $DIR/../rplugin/python/vim_matlab
python -m unittest discover
