#!/bin/bash

cd ../../
source .venv/bin/activate
python -m pip uninstall p115
deactivate
rm -rf .venv data
