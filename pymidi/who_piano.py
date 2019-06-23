import pygame.midi
import mido
from mido import Message, MidiFile, MidiTrack
import sys
import time

arr_midi = []
track = MidiTrack()
mid = MidiFile()

def print_devices():
    for n in range(pygame.midi.get_count()):
        print (n,pygame.midi.get_device_info(n))

def number_to_note(number):
    notes = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
    return notes[number%12]

def readInput(input_device):
	arr_final_midi = []
	going = True
	while going:
		if input_device.poll():

			event = input_device.read(1)[0]
			arr_midi.append(event)
			data = event[0]
			id_note = data[0]
			note_number = data[1]
			velocity = data[2]
			#if id_note == 144:

			if(note_number != 0 or note_number != 254):
				miditime = int(round(mido.second2tick(0,mid.ticks_per_beat, mido.bpm2tempo(120))))
				print (event)
			if(note_number == 100):
				going = False

	#pygame.midi.quit()
	if len(arr_midi)>1024:
		for i in range(0,1024):
			arr_final_midi[i] = arr_midi[i]
	else:
		arr_final_midi = arr_midi
	#leid = pygame.midi.get_default_output_id()
	#hola = pygame.midi.Output(leid, 0)
	#hola.write(arr_final_midi)


#def inputLine(timestamp1, timestamp2):
	#delta_timestamp = timestamp2 - timestamp1
	#if (delta_timestamp < )

def readAndTransformInput(input_device):
    while True:
        if input_device.poll():
            event = input_device.read(1)[0]
            data = event[0]
            timestamp = event[1]
            note_number = data[1]
            velocity = data[2]
            if(note_number != 248):
            	print (number_to_note(note_number), velocity, note_number)
            	

#if __name__ == '__main__':


pygame.midi.init()
while True:
	print_devices()
	time.sleep(2)
#if len(sys.argv)<2:
#	print("Especifique el nombre del piano")
#	print_devices()
#	pygame.midi.quit()
#	sys.exit(0)
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

try:
	for num in num_device:
		my_input = pygame.midi.Input(num)
		readInput(my_input)
except KeyboardInterrupt:
	pygame.midi.quit()
finally:
	pygame.midi.quit()