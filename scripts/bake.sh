#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env ]; then
	source .env
fi
echo $QUBE_SERVICE_DOCKER_IMAGE_LOCAL

docker build -t $QUBE_SERVICE_DOCKER_IMAGE_LOCAL:$QUBE_SERVICE_IMAGE_VERSION . 
