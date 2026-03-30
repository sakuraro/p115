#!/bin/bash

script_path=$(cd "$(dirname "$(readlink -f "$0")")";pwd)
cd "$script_path/../../"
mkdir data
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
deactivate
