# TJ Heat

## Game
### Dependencies

- python 3.10.4
- arcade 2.6.15
- [Tiled 1.9.1](https://www.mapeditor.org/)



### Install instructions

Setup has been based around virtual environments, with some provided scripts assisting the process.

Steps:

1. Install [python](https://www.python.org/downloads/).
2. Enable execution of scripts with `chmod +x scripts/*`.
3. Run environment setup script `scripts/setup.sh` from the top level directory of the repo. 
   - For Windows Command Prompt, use `scripts/batch/setup.bat` instead.
4. Apply patches based on installed packages by running `scripts/apply_patches.sh`.
   - There is no Command Prompt alternative file. 



### Development

#### Starting Working

When working on the project, development should be carried out inside of the virtual environment. There are several ways of doing so.

- From the terminal:
  1. From the top of the repo, run `source env/Scripts/activate`. Change the activation script used to suit your dev environment (OS/shell).
     - `source env/bin/activate` for non-Windows.
  2. When finished, run `deactivate` to finish with the virtual environment.
- From VS-Code:
  1. Open the repository folder (default "signed-explorations") in VS-Code. It is important to open the ENTIRE directory with VS-Code.
  2. Open the Command Palette with `Ctrl+Shift+P` (`Cmd+Shift+P` for Mac users).
  3. Search for `Python: Select Interpreter`.
  4. From the provided options, select the Python version listed as `('env': venv)`. It should be the recommended option.

#### Installing New Packages

If your environment's packages are out of date, simply run `scripts/update_packages.sh` from the top level of the repo. A `.bat` is provided for Command Prompt.

If you have added a new package for development, run `scripts/add_packages.sh` from the top level of the repo; then, commit the changed `requirements.txt` file. A `.bat` is provided for Command Prompt in `scripts/batch/`.

#### Development Example

An example of running the setup process in a \*Nix-style terminal environment.  

``` shell
git clone https://github.com/tj-heat/signed-explorations.git
cd signed-explorations
chmod +x scripts/*
scripts/setup.sh
scripts/apply_patches.sh

# To begin development
source env/bin/activate
...
# To finish development
#(env)
deactivate
```

#### Development Guides

- Physics engine: [Pymunk Platformer Tutorial](https://api.arcade.academy/en/latest/tutorials/pymunk_platformer/index.html)
- Top Down Implementation: [Pymunk Top Down Tutorial](https://api.arcade.academy/en/latest/examples/pymunk_demo_top_down.html)
- Scene, Screen, and basics: [Arcade Platformer Tutorial](https://api.arcade.academy/en/latest/examples/platform_tutorial/index.html)



### Run Game

Open signed-explorations directory in preferred terminal and run:

``` shell
env/Scripts/python.exe main.py
```



## Team Members

- Ethan Roderick, 44792215.
- Treffery Webb, 4503374.
- Hannah Hinckfuss, 45840047
- Joseph Metcalfe, 44822279
- Aditya Modi, 45892046
- Thomas Webber, 44349945
