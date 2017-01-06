#!/usr/bin/python
# -*- coding: utf8 -*-
# 11 mars 2015 - Tristan Le Toullec  


# PopCorn.py : Make a video from pictures dropped in a directory.
# Author : Tristan Le Toullec - tristan dot letoullec at univ dash brest dot fr
# Licence : GPLv3
#
# Please keep PEP 8
#
""" PopCorn.py : Make a video from pictures dropped in a directory.

To finish video "recording", press crtl+c or send a file with filename
contains "THEEND"
"""

import Queue
import argparse
import cv2
import os
import pyinotify
import threading
import time

video = None

parser = argparse.ArgumentParser(description="PopCorn.py - Wait pictures in a \
                                 directory, appends it to a video file.")

parser.add_argument("-i", "--input", dest="frames",
                    help="Which folder did I watch")
parser.add_argument("-o", "--output", dest="videofile", default="output.avi",
                    help="Output video file")
parser.add_argument("--fps", dest="fps", default=24.0,
                    help="Frames per second")
parser.add_argument("-x", dest="erase", action='store_true',
                    help="Erase sources frames after processing")

args = parser.parse_args()


def create_video():
    """ Cette fonction est un thread, une boucle sans fin lit la pile FIFO q
    et en sort la reference du fichier a traiter. Cette fonction attend qu'il
    y ai au minimun deux fichiers dans la pile car l'evenement nouveau fichier
    engendre par pyinotify se declenche a la creation du fichier et non lorsque
    celui ci est termine.
    """
    global video

    record = True
    while record:
        if q.qsize() > 1:
            framefile = str(q.get())
            print("addFrame "+framefile)
            img = cv2.imread(framefile)

            try:
                """ ecrtiure de la frame sur la video """
                video.write(img)
            except:
                """ impossible d'ecrire la frame dans la video > la video n'est
                pas cree > creation de la video """
                height , width , layers =  img.shape
                print(height , width , layers)
                fourcc = cv2.VideoWriter_fourcc(*'MJPG')
                video = cv2.VideoWriter(args.videofile,
                                        fourcc,
                                        float(args.fps),
                                        (width,height))
                video.write(img)
            if args.erase:
                """ si l'args -x est OK, on efface les fichiers de donnees
                apres integration
                """
                os.remove(framefile)
            q.task_done()
        time.sleep(0.1)


class PTmp(pyinotify.ProcessEvent):
    """ cette class recoit les notifications de creation de nouveau fichier
    et les envois dans pile FIFO q
    """
    def process_IN_CREATE(self, event):
        if "THEEND" in os.path.join(event.path, event.name):
            """ detecte le fichier de sortie, le filename doit comporter
            THEEND """

            while q.qsize() != 1:
                """Il faut attendre que le thread de construction de la video
                finisse sa pile
                """
                time.sleep(1)
            #Sometime createVideo take long time to write end-1 frame
            time.sleep(5)

            video.release()

            print(q.qsize())
            print('The end, get pop-corns...')
            raise Exception('THEEND')
        else:
            q.put(os.path.join(event.path, event.name))

mask = pyinotify.IN_CREATE
wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm, PTmp())
wdd = wm.add_watch(args.frames, mask, rec=True)

q = Queue.Queue()

# Creation du thread d' ajout de frames dans la video
t = threading.Thread(target=create_video)
t.daemon = True
t.start()

while True:
    try:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()
    except Exception as e:
        notifier.stop()
        # Delete THEEND file
        try:
            framefile = str(q.get())
            os.remove(framefile)
            pass
        except:
            pass
        break