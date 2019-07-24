import pygame.midi
import mido
from mido import Message, MidiFile, MidiTrack
import sys
import time

def print_devices():
    for n in range(pygame.midi.get_count()):
        print (n,pygame.midi.get_device_info(n))

def readInput(input_device):
	#going = True
	#while going:
	if input_device.poll():

		event = input_device.read(1)[0]
		data = event[0]
		id_note = data[0]
		note_number = data[1]
		velocity = data[2]
		time = event[1]
		#if id_note == 144:
		note_status = transform_id(id_note)

		if(note_number != 0 or note_number != 254):
			#miditime = int(round(mido.second2tick(0,mid.ticks_per_beat, mido.bpm2tempo(120))))
			print (note_number, note_status, time)

def transform_id(id_note):
	if id_note == 144:
		return "note_on"
	elif id_note == 128:
		return "note_off"
	else:
		return "invalid"

pygame.midi.init()
print_devices()

arr_name = [""]*pygame.midi.get_count()
arr_device = [""]*pygame.midi.get_count()
arr_input = [""]*pygame.midi.get_count()
arr_output = [""]*pygame.midi.get_count()
arr_active = [""]*pygame.midi.get_count()
num_device = []

for n in range(pygame.midi.get_count()):
    (aux_name, aux_device, aux_input, aux_output, aux_active) = pygame.midi.get_device_info(n)
    arr_name[n] = aux_name
    arr_device[n] = aux_device
    arr_input[n] = aux_input
    arr_output[n] = aux_output
    arr_active[n] = aux_active
print(arr_input)
for n in range(pygame.midi.get_count()):
	aux = arr_input[n]
	aux_int = int(aux)
	if(aux_int == 1):
		num_device.append(n)
my_input = pygame.midi.Input(num_device[0])

try:
	readInput(my_input)
except KeyboardInterrupt:
	del my_input
finally:
	pygame.midi.quit()