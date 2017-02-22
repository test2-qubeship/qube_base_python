#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
set -o allexport
#load .env.sh. switch dir to make 'cat ./qube.yaml' work
pushd ..
source .env.sh
popd

echo "checkout /tmp/test.out for info"
echo "checkout /tmp/error.out for errors"

rm /tmp/test.out 2> /dev/null
rm /tmp/error.out 2> /dev/null

bats tests.bats
