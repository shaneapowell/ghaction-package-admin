#!/bin/bash

CLI_ARGS=$@

echo "Starting Action with args [ ${CLI_ARGS} ]"

cd /action

echo "Running Action"
python ghpkgadmin.py ${CLI_ARGS}
