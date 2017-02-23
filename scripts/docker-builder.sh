#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..
docker run -i --rm --name python3-builder -v "$PWD":/usr/src/myapp -v /usr/src/myapp/.tox -v /usr/src/myapp/build -w /usr/src/myapp python:3.5-onbuild scripts/build.sh
