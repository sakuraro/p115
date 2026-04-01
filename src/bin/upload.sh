#!/bin/bash

script_path=$(dirname "$(readlink -f "$0")")
local_path=$(readlink -f "$1")

cd "$script_path/../../"
source .venv/bin/activate
python -m p115 upload -l "$local_path" -r "$2"
deactivate
