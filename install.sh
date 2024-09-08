#!/bin/bash

PROJECT_DIR="$HOME/.aniwatch-tr"

cd "$PROJECT_DIR" 
chmod +x "$PROJECT_DIR/aniwatch-tr"

cd "$PROJECT_DIR"/.aniwatch-tr && sudo python3 -m venv .venv
cd "$PROJECT_DIR"/.aniwatch-tr && sudo .venv/bin/pip3 install requests inquirer
