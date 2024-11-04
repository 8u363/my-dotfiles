#!/bin/bash

stow config --adopt  --target "/home/$USER/.config"
betterlockscreen -u "/home/$USER/.config/qtile/wallpaper/default.jpg"