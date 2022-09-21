#!/bin/bash

# Install packages in venv
./env/Scripts/pip.exe install -r ./requirements.txt || 
	./env/bin/pip install -r ./requirements.txt
