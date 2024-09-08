#!/bin/bash

sudo chmod +x aniwatch-tr/aniwatch-tr

cd aniwatch-tr && sudo python3 -m venv .venv
cd aniwatch-tr && sudo .venv/bin/pip3 install requests inquirer
