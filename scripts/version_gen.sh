#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..
if [ -z "$QUBE_BUILD_VERSION" ]; then
    git log --decorate=short --pretty=oneline  | grep "$branch" | head -1 | awk '{print substr($1,0,7)"-" $4}' | sed "s/,//g" | sed "s/)//g"> qube/src/resources/qube_version.txt
else
    echo "$QUBE_BUILD_VERSION" > qube/src/resources/qube_version.txt
fi