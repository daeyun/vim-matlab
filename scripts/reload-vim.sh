#!/bin/bash

set -o xtrace

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

find $DIR/../rplugin/python -type f -name '*.pyc' -exec rm {} \;
find $DIR/../rplugin/python -type d -name '__pycache__' -exec rm {} \;
nvim -c "UpdateRemotePlugins" -c "q" && nvim $@ -c "UpdateRemotePlugins"
