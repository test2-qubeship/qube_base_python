#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $DIR
cd $DIR/..
set -o allexport
#load .env.sh. switch dir to make 'cat ./qube.yaml' work
#pushd ..
source .env
#popd

echo "checkout /tmp/test.out for info"
echo "checkout /tmp/error.out for errors"

rm /tmp/test.out 2> /dev/null
rm /tmp/error.out 2> /dev/null

bats bats/tests.bats
