[![Rye](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/mitsuhiko/rye/main/artwork/badge.json)](https://rye-up.com)

# terminator-image-swapper

![Terminator pic](terminator2.jpg)

## About
A simple script to change the background picture of [terminator](https://github.com/gnome-terminator/terminator) terminal.

## Install 
```
git clone git@github.com:AtomsForPeace/terminator-image-swapper.git
cd terminator-image-swapper
rye sync
```

## Config
Start by setting the path to the folder where your image are:
```
rye run set_image_folder /path/to/my/image/folder
```

Then simply run the following for the image to randomly change:
```
rye run random_image
```
