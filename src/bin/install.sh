#!/bin/bash

cd ../../
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
deactivate
