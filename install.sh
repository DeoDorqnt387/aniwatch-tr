#!/bin/bash

PROJECT_DIR="$HOME/.aniwatch-tr"

chmod +x $PROJECT_DIR/aniwatch-tr

cd $PROJECT_DIR 
python3 -m venv .venv 
.venv/bin/pip install requests inquirer

sudo chmod +x /usr/local/bin/aniwatch-tr
