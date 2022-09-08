#!/bin/bash

# Set up virtual environment
py -m venv ./env
# Install packages
./env/Scripts/pip.exe install -r ./requirements.txt