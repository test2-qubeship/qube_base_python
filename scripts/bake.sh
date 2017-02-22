#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env.sh ]; then
	source .env.sh
fi
echo $QUBE_DOCKER_IMAGE_LOCAL

docker build -t $QUBE_DOCKER_IMAGE_LOCAL .
