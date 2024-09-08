#!/bin/bash

PROJECT_DIR="$HOME/.aniwatch-tr"

chmod +x $PROJECT_DIR/aniwatch-tr

cd ~/.aniwatch-tr && sudo python3 -m venv .venv
cd ~/.aniwatch-tr && sudo .venv/bin/pip install requests inquirer
