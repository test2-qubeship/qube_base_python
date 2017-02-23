#!/bin/bash
set -o allexport
export PYTHONPATH=$PWD
source .env
#source env/bin/activate
export DEBUG=true
python -m qube.src.api.app
