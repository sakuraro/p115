#!/bin/bash

script_path=$(dirname "$(readlink -f "$0")")

cd "$script_path/../../"
mkdir data
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
deactivate
