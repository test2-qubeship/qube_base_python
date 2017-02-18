#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
set -o allexport
source $DIR/../.env.sh
echo "checkout /tmp/test.out for info"
echo "checkout /tmp/error.out for errors"

bats tests.bats