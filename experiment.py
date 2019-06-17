# This is an script example of how to use the pytribe.EyeTribe class to track
# gaze data while a participant is looking at some images. Please note that
# the experiment assumes that you have calibrated the eye tracker beforehand,
# using the EyeTribe UI.
#
# Data analysis will be performed directly after running the experiment, using
# PyGazeAnalyser (see: https://github.com/esdalmaijer/PyGazeAnalyser)
#
# The folder in which this script is placed, should contain the following:
#       - experiment.py (this script)
#       - analysis.py (data analysis script)
#       - pytribe.py (script to communicate with the EyeTribe tracker,
#               from: https://github.com/esdalmaijer/PyTribe/blob/master/pytribe.py)
#       - imgs (folder containing images,
#               from: https://github.com/esdalmaijer/PyGazeAnalyser/tree/master/examples/analysis/imgs)
#       - pygazeanalyser (folder containing analysis routines for gaze data,
#               from: https://github.com/esdalmaijer/PyGazeAnalyser/tree/master/pygazeanalyser)
#
# author: Edwin Dalmaijer
# email: edwin.dalmaijer@psy.ox.ac.uk
#
# version 1 (02-Jul-2014)

# native
import os

# external
import pygame
import time
# custom
from pytribe import EyeTribe
from pymidi import recorder as rec
#from pymidi.CK_rec import all
#import time
import rtmidi
#import from parrentdir
import sys
#import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from pymidi.CK_rec.setup import Setup
from pymidi.CK_rec.rec_classes import CK_rec

# # # # #
# CONSTANTS

# screen stuff
RESOLUTION = (1280,1024)
BGC = (0,0,0)

# files and paths
DIR = os.path.dirname(os.path.abspath(__file__))
LOGFILE = os.path.join(DIR, 'example_data.txt')
IMGDIR = os.path.join(DIR, 'imgs')
IMGNAMES = os.listdir(IMGDIR)


# # # # #
# PREPARE

# start communications with the EyeTribe tracker
tracker = EyeTribe(logfilename=LOGFILE)

#try to use pymidi

# initialize PyGame
pygame.init()

# create a new display
disp = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)

# compile a list of images
images = {}
for filename in IMGNAMES:
        # check if the extension is a JPEG image
        if os.path.splitext(filename)[1] == '.jpg':
                # load the image, and add to the image dict
                images[filename] =  pygame.image.load(os.path.join(IMGDIR,filename))


# # # # #
# RUN
id_record = 0
name_record = "loco_"
# loop through all images
for imgname in images.keys():
        
        # blit the image
        blitpos = (RESOLUTION[0]/2 - images[imgname].get_width()/2,
                        RESOLUTION[1]/2 - images[imgname].get_height()/2)
        disp.blit(images[imgname], blitpos)

        # start recording gaze data
        tracker.start_recording()


        # show the image
        pygame.display.flip()
        tracker.log_message("image_on")
        tracker.log_message(imgname)

        # start recording midi data
        codeK = Setup()
        #myPort = codeK.perform_setup()
        myPort = 0
        codeK.open_port(myPort)
        on_id = 144
        midiRec = CK_rec(myPort, on_id)
        codeK.set_callback(midiRec)
        id_record += 1
        # wait for a bit
        # pygame.time.wait(5000)
        # show a blank screen
        disp.fill(BGC)
        evkey = True
        while evkey:
            time.sleep(0.001)
            events = pygame.event.get()
            for event in events:
                    if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                    evkey = False
                                    name = name_record + str(id_record)
                                    if name != "":
                                        midiRec.saveTrack(name)
                                    codeK.end()
                                    pygame.display.flip()
                                    tracker.log_message("image_off")
                                    tracker.stop_recording()
        #rec.save(id_record,"veamos")
                #if event.key == pygame.K_RIGHT:
                    #location += 1
        # stop recording
        #tracker.stop_recording()

        # wait for a bit
        #pygame.time.wait(2000)

# # # # #
# CLOSE

# close connection to the tracker
tracker.close()

# close the display
pygame.quit()
