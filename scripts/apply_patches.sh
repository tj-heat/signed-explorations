#!/bin/bash
patch env/Lib/site-packages/pytiled_parser/parsers/json/tiled_object.py < \
	_patches/tiled_object.py.patch ||
patch "env/lib/python3.10/site-packages/pytiled_parser/parsers/json/tiled_object.py" < \
	_patches/tiled_object.py.patch

patch env/Lib/site-packages/arcade/pymunk_physics_engine.py < \
	_patches/pymunk_physics_engine.py.patch ||
patch "env/lib/python3.10/site-packages/arcade/pymunk_physics_engine.py" < \
	_patches/tiled_object.py.patch
