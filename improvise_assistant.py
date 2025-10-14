import fluidsynth
import pygame
import threading
import time

TEMPO = 140

NOTES = {
	"whole": 1.0,
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

	return note_dict

MIDI_NAMES = create_midi_note_dict()

pygame.init()
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Improvise Assistant")

def note_duration_seconds(length_fraction):
	seconds_per_beat = 60 / TEMPO
	return length_fraction * 4 * seconds_per_beat

def play_notes(notes: list, bank: int = 0, preset: int = 0):
	synth = fluidsynth.Synth()
	synth.start()

	sfid = synth.sfload("assets/ms-basic.sf2")
	synth.program_select(0, sfid, bank, preset)

	for note, length_fraction in notes:
		note = MIDI_NAMES[note]
		length_fraction = NOTES[length_fraction]
		note_duration = note_duration_seconds(length_fraction)
		synth.noteon(0, note, 100)
		time.sleep(note_duration)
		synth.noteoff(0, note)
	
	synth.delete()

def play_song(song_dict: dict):
	synth = fluidsynth.Synth()
	synth.start()

	sfid = synth.sfload("assets/ms-basic.sf2")
	for instrument, measures in song_dict.items():
		if instrument == "harp":
			bank = 0; preset = 46; channel = 0
		elif instrument == "piano":
			bank = 0; preset = 0; channel = 1
		elif instrument == "drums":
			bank = 128; preset = 32; channel = 2
		
		synth.program_select(channel, sfid, bank, preset) # type: ignore
		
		for measure in measures:
			for note_name, note_length in measure:
				note_name = MIDI_NAMES[note_name]
				note_length = NOTES[note_length]
				note_dur = note_duration_seconds(note_length)
				synth.noteon(channel, note_name, 100) # type: ignore
				time.sleep(note_dur)
				synth.noteoff(channel, note_name) # type: ignore
		
	synth.delete()

formula_song = {
	"piano": [
		[("C3", "quarter-dotted"), ("D#3", "eighth"), ("G3", "half")],
		[("G2", "quarter-dotted"), ("A#2", "eighth"), ("F3", "half")]
	]
}

threading.Thread(target=play_song, args=(formula_song,), daemon=True).start()

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	
	screen.fill((50, 50, 50))
	pygame.display.flip()

pygame.quit()