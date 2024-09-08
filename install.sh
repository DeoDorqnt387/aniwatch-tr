#!/bin/bash

PROJECT_DIR="$HOME/.aniwatch-tr"

chmod +x $PROJECT_DIR/main.py
chmod 755 $PROJECT_DIR
chmod 755 $PROJECT_DIR/*

cd $PROJECT_DIR
python3 -m venv .venv
.venv/bin/pip install requests inquirer

echo 'export PATH="$HOME/.aniwatch-tr/.venv/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

echo -e '#!/bin/bash\n'\
'. '$PROJECT_DIR'/.venv/bin/python '$PROJECT_DIR'/main.py' | sudo tee /usr/local/bin/aniwatch-tr
sudo chmod +x /usr/local/bin/aniwatch-tr
