#!/usr/bin/env python3
from animeci import animecix
from openani import Openani
import tools

def main():
    app = animecix()
    openani = Openani()
    selection = tools.display_website_selection_thing()
    if selection == "AnimeciX (ID: 856)":
        app.srch_anime()
    else:
        openani.srch_anime()


if __name__ == "__main__":
    main()
