import time
import rtmidi
#import from parrentdir
import sys
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
from pymidi.CK_rec.setup import Setup
from pymidi.CK_rec.rec_classes import CK_rec



# Start the Device
#def record():
codeK = Setup()
myPort = codeK.perform_setup()
codeK.open_port(myPort)
on_id = 144
midiRec = CK_rec(myPort, on_id)
codeK.set_callback(midiRec)
# Loop to program to keep listening for midi input
try:
	while True:
		time.sleep(0.001)
except KeyboardInterrupt:
	print('')
finally:
	name = input('\nsave midi recording as? (leaving the name blank discards the recording): ')
	#name = name_record + str(id_record)
	if name != "":
		midiRec.saveTrack(name)
	codeK.end()