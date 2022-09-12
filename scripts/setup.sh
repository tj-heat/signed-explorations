#!/bin/bash

# Use variable to indicate install system
WIN=true

# Set up virtual environment
echo "Attempting Windows style setup..."
if ! (py -m venv ./env) ; then
	WIN=false
	echo "Attempting *Nix style setup..."
	python -m venv ./env
fi

# Install packages
if $WIN = true ; then
	echo "Attempting Windows style install..."
	./env/Scripts/pip.exe install -r ./requirements.txt
else
	echo "Attempting *Nix style install..."
	./env/bin/pip install -r ./requirements.txt
fi
