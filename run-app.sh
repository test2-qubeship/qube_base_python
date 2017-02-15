#!/bin/bash
set -o allexport
export PYTHONPATH=$PWD
source .env.sh
source env/bin/activate
python -m qube.src.api.app
