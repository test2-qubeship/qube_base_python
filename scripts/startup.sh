#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/

set -o allexport
source env-init.sh

python -m qube.src.api.app --debug 2>&1 > nohup.out
tail -f nohup.out