#!/bin/bash

PROJECT_DIR="$HOME/.aniwatch-tr"
cd "$PROJECT_DIR" || exit

chmod +x "$PROJECT_DIR/aniwatch-tr"

python3 -m venv .venv
source .venv/bin/activate
pip3 install requests inquirer
