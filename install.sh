#!/bin/bash

sudo chmod +x aniwatch-tr/aniwatch-tr
sudo mv aniwatch-tr/aniwatch-tr /usr/local/bin

cd /.aniwatch-tr && sudo python3 -m venv .venv
cd /.aniwatch-tr && sudo .venv/bin/pip install requests inquirer
