#!/bin/bash

# Add packages to requirements
./env/Scripts/pip.exe freeze > ./requirements.txt || 
	./env/bin/pip freeze > ./requirements.txt
