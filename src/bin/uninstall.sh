#!/bin/bash

script_path=$(cd "$(dirname "$(readlink -f "$0")")";pwd)
cd "$script_path/../../"
source .venv/bin/activate
python -m pip uninstall p115
deactivate
rm -rf .venv data
