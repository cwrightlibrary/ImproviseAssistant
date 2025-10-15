import os

os.add_dll_directory(r"C:\Users\circ8\Documents\Chris\fluidsynth-v2.5.0-win10-x64-cpp11\bin")

import fluidsynth
import pygame
import threading
import time

TEMPO = 140
CURRENT_MEASURE = 1

NOTES = {
	"whole": 1.0,
	"half-dotted-eighth-tie": 0.875,
	"half-dotted": 0.75,
	"half": 0.5,
	"quarter-dotted": 0.375,
	"quarter": 0.25,
	"eighth-dotted": 0.1875,
	"eighth": 0.125
}

def create_midi_note_dict() -> dict:
	note_dict = {}
	nnames = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
	st_octave = 1; end_octave = 6
	
	for octave in range(st_octave, end_octave + 1):
		for i, note in enumerate(nnames):
			midi_num = (octave + 1) * 12 + i
			note_name = f"{note}{octave + 1}"
			note_dict[note_name] = midi_num
			if note == "C#":
				note_dict["Db"] = midi_num
			elif note == "D#":
				note_dict["Eb"] = midi_num
			elif note == "F#":
				note_dict["Gb"] = midi_num
			elif note == "G#":
				note_dict["Ab"] = midi_num
			elif note == "A#":
				note_dict["Bb"] = midi_num

	return note_dict

MIDI_NAMES = create_midi_note_dict()

pygame.init()
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Improvise Assistant")

font = pygame.font.SysFont(None, 100)
text = font.render(str(CURRENT_MEASURE), True, (255, 255, 255))
text_rect = text.get_rect(center=(300 // 2, 300 // 2))

def note_duration_seconds(length_fraction):
	seconds_per_beat = 60 / TEMPO
	return length_fraction * 4 * seconds_per_beat

def play_instrument(instrument, measures, sfid, synth):
	if instrument == "harp":
		bank = 0; preset = 46; channel = 0
	elif instrument == "piano":
		bank = 0; preset = 0; channel = 1
	elif instrument == "piano2":
		bank = 0; preset = 0; channel = 3
	elif instrument == "drums":
		bank = 128; preset = 32; channel = 2
	else:
		return
	
	synth.program_select(channel, sfid, bank, preset)

	global CURRENT_MEASURE, text, text_rect
	for midx, measure in enumerate(measures):
		for note_name, note_len in measure:
			velocity = 100

			if isinstance(note_name, str) and note_name.lower() == "r":
				note_name = "C3"
				velocity = 0
			
			if isinstance(note_name, list):
				note_name = [MIDI_NAMES[n] for n in note_name]
			else:
				note_name = MIDI_NAMES[note_name]
			
			note_len = NOTES[note_len]
			note_dur = note_duration_seconds(note_len)

			if isinstance(note_name, list):
				for n in note_name:
					synth.noteon(channel, n, velocity)
				time.sleep(note_dur)
				for n in note_name:
					synth.noteoff(channel, n)
			else:
				synth.noteon(channel, note_name, velocity)
				time.sleep(note_dur)
				synth.noteoff(channel, note_name)
		
		CURRENT_MEASURE = midx + 1
		text = font.render(str(CURRENT_MEASURE + 1), True, (255, 255, 255))
		text_rect = text.get_rect(center=(300 // 2, 300 // 2))

def play_song(song_dict: dict):
	synth = fluidsynth.Synth()
	synth.start()
	sfid = synth.sfload("assets/ms-basic.sf2")

	threads = []
	for instrument, measures in song_dict.items():
		t = threading.Thread(target=play_instrument, args=(instrument, measures, sfid, synth))
		t.start()
		threads.append(t)
	
	for t in threads:
		t.join()
	
	synth.delete()

formula_song = {
	"piano": [
		[("C3", "quarter-dotted"), ("D#3", "eighth"), ("G3", "half")],
		[("G2", "quarter-dotted"), ("A#2", "eighth"), ("F3", "quarter-dotted"), ("G2", "eighth")],
		[("F2", "quarter-dotted"), ("C3", "eighth"), ("D#3", "half")],
		[("F2", "quarter-dotted"), ("C3", "eighth"), ("D#3", "quarter-dotted"), ("D3", "eighth")],
		[("C3", "quarter-dotted"), ("D#3", "eighth"), ("G3", "half")],
		[("G2", "quarter-dotted"), ("A#2", "eighth"), ("F3", "quarter-dotted"), ("G2", "eighth")],
		[("F2", "quarter-dotted"), ("C3", "eighth"), ("D#3", "half")],
		[("F2", "quarter-dotted"), ("C3", "eighth"), ("D#3", "quarter-dotted"), ("D3", "eighth")],
		[("C3", "quarter-dotted"), ("D#3", "eighth"), ("G3", "half")],
		[("F2", "quarter-dotted"), ("C3", "eighth"), ("D#3", "quarter-dotted"), ("D3", "eighth")],
		[("G#2", "quarter-dotted"), ("C3", "eighth"), ("G3", "half")],
		[("G#2", "quarter-dotted"), ("C3", "eighth"), ("G3", "quarter-dotted"), ("D#3", "eighth")],
		[("C3", "quarter-dotted"), ("D#3", "eighth"), ("G3", "half")],
		[("G2", "quarter-dotted"), ("A#2", "eighth"), ("F3", "quarter-dotted"), ("G2", "eighth")],
		[("F2", "quarter-dotted"), ("C3", "eighth"), ("D#3", "half")],
		[("F2", "quarter-dotted"), ("C3", "eighth"), ("D#3", "quarter-dotted"), ("D3", "eighth")]
	],
	"piano2": [
		[("R", "eighth"), (["C5", "D#5", "G5", "A#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["A#4", "D5", "F5", "G#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["C5", "D#5", "F5", "G#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["C5", "D#5", "F5", "G#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["C5", "D#5", "G5", "A#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["A#4", "D5", "F5", "G#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["C5", "D#5", "F5", "G#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["C5", "D#5", "F5", "G#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["C5", "D#5", "G5", "A#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["C5", "D#5", "F5", "G#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["C5", "D#5", "G5", "G#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["C5", "D#5", "G5", "G#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["C5", "D#5", "G5", "A#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["A#4", "D5", "F5", "G#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["C5", "D#5", "F5", "G#5"], "half-dotted-eighth-tie")],
		[("R", "eighth"), (["C5", "D#5", "F5", "G#5"], "half-dotted-eighth-tie")]
	],
	"harp": [
		[("R", "quarter"), (["C6", "A#6"], "eighth"), (["C6", "A#6"], "eighth"), ("R", "quarter"), (["C6", "A#6"], "eighth"), ("R", "eighth")],
		[(["G5", "F6"], "quarter-dotted"), ("R", "quarter-dotted"), (["G5", "F6"], "eighth"), (["G5", "F6"], "eighth")],
		[(["F5", "D#6"], "eighth"), ("R", "eighth"), (["F5", "D#6"], "eighth"), ("R", "quarter"), (["F5", "D#6"], "eighth"), ("R", "quarter")],
		[(["F5", "D#6"], "eighth"), (["F5", "D#6"], "eighth"), ("R", "half-dotted")],
		[("R", "quarter"), (["C6", "A#6"], "eighth"), (["C6", "A#6"], "eighth"), ("R", "quarter"), (["C6", "A#6"], "eighth"), ("R", "eighth")],
		[(["G5", "F6"], "quarter-dotted"), ("R", "quarter-dotted"), (["G5", "F6"], "eighth"), (["G5", "F6"], "eighth")],
		[(["F5", "D#6"], "eighth"), ("R", "eighth"), (["F5", "D#6"], "eighth"), ("R", "quarter"), (["F5", "D#6"], "eighth"), ("R", "quarter")],
		[(["F5", "D#6"], "eighth"), (["F5", "D#6"], "eighth"), ("R", "half-dotted")],
		[(["C6", "A#6"], "eighth"), ("R", "eighth"), (["C6", "A#6"], "eighth"), ("R", "quarter"), (["C6", "A#6"], "eighth"), ("R", "quarter")],
		[("R", "eighth"), (["F5", "D#6"], "eighth"), ("R", "quarter"), (["F5", "D#6"], "quarter-dotted"), ("R", "eighth")],
		[(["G#5", "G6"], "eighth"), ]
	]
}

threading.Thread(target=play_song, args=(formula_song,), daemon=True).start()

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	screen.fill((50, 50, 50))
	screen.blit(text, text_rect)
	pygame.display.flip()

pygame.quit()