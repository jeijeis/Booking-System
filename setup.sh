#!/bin/bash
# Install virtual display + Qt dependencies
sudo apt-get update -y
sudo apt-get install -y \
  xvfb \
  libxcb-cursor0 \
  libxcb-icccm4 \
  libxcb-image0 \
  libxcb-keysyms1 \
  libxcb-randr0 \
  libxcb-render-util0 \
  libxcb-xinerama0 \
  libxcb-xkb1 \
  libxkbcommon-x11-0 \
  libgl1-mesa-glx \
  libegl1

pip install PySide6