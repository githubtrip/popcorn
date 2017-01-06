Popcorn.py
==========

Popcorn.py make video from images. PopCorn.py - Wait pictures in a directory, appends it to a video file

Requirements
------------

* OpenCV
* libnetcdf-dev
* Python librairies are documented inside requirements.txt

```
pip install -r requirements.txt
```

Usage
-----

```
usage: popcorn.py [-h] [-i FRAMES] [-o VIDEOFILE] [--fps FPS] [-x]

PopCorn.py - Wait pictures in a directory, appends it to a video file.

optional arguments:
  -h, --help            show this help message and exit
  -i FRAMES, --input FRAMES
                        Which folder did I watch
  -o VIDEOFILE, --output VIDEOFILE
                        Output video file
  --fps FPS             Frames per second
  -x                    Erase sources frames after processing
```

Exemple :
```
python popcorn.py --input ./frames/ --ouput output.avi --fps=24.0 -x
```

Test
----

go.py is a simple script which needs etopo2.nc bathymetric data. It generate frame insides a frames directory.

Test need this file :
ftp://ftp.ifremer.fr/ifremer/cersat/products/gridded/wavewatch3/pub/COURS/WAVE_DATA/gridgen/reference_data/etopo2.nc

