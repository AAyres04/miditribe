import pygame.midi
import mido
import sys
import time

class PianoRecord():

	def print_devices(self):
	    for n in range(pygame.midi.get_count()):
	        print (n,pygame.midi.get_device_info(n))


	def readInput(self, input_device):
		if input_device.poll():

			event = input_device.read(1)[0]
			data = event[0]
			id_note = data[0]
			note_number = data[1]
			velocity = data[2]
			time = event[1]
			#if id_note == 144:
			note_status = self.transform_id(id_note)

			if(note_number != 0 or note_number != 254):
					#miditime = int(round(mido.second2tick(0,mid.ticks_per_beat, mido.bpm2tempo(120))))
				print (note_number, note_status, time)


	def transform_id(self, id_note):
		if id_note == 144:
			return "note_on"
		elif id_note == 128:
			return "note_off"
		else:
			return "invalid"

	def __init__(self):
		pygame.midi.init()
		self.print_devices()
		self.__arr_name = [""]*pygame.midi.get_count()
		self.__arr_device = [""]*pygame.midi.get_count()
		self.__arr_input = [""]*pygame.midi.get_count()
		self.__arr_output = [""]*pygame.midi.get_count()
		self.__arr_active = [""]*pygame.midi.get_count()
		self.__num_device = []
		self.__my_input = self.set_piano()

	def search_piano(self):
		for n in range(pygame.midi.get_count()):
		    (aux_name, aux_device, aux_input, aux_output, aux_active) = pygame.midi.get_device_info(n)
		    self.__arr_name[n] = aux_name
		    self.__arr_device[n] = aux_device
		    self.__arr_input[n] = aux_input
		    self.__arr_output[n] = aux_output
		    self.__arr_active[n] = aux_active
		print(self.__arr_input)
		for n in range(pygame.midi.get_count()):
			aux = self.__arr_input[n]
			aux_int = int(aux)
			if(aux_int == 1):
				self.__num_device.append(n)
		return self.__num_device[0]

	def set_piano(self):
		num = self.search_piano()
		my_input = pygame.midi.Input(num)
		return my_input

	def stop_recording(self):
		del self.__my_input
		pygame.midi.quit()

	def start_recording(self):
		self.readInput(self.__my_input)