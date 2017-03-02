#!/bin/bash
pip install tox wheel
pip list
tox
scripts/version_gen.sh
python setup.py bdist_wheel