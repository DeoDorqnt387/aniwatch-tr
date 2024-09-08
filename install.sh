#!/bin/bash

sudo chmod +x aniwatch-tr/aniwatch-tr
sudo chmod 755 aniwatch-tr
sudo chmod 755 aniwatch-tr/*

cd aniwatch-tr || exit
python3 -m venv .venv
.venv/bin/pip3 install requests inquirer
