#!/bin/bash

script_path=$(cd "$(dirname "$(readlink -f "$0")")";pwd)
cd "$script_path/../../"
source .venv/bin/activate
local_path="$(readlink -f $1)"
flock /tmp/p115.lock -c "python -m p115 upload -l \"$local_path\" -r \"$2\""
deactivate
