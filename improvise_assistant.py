import pygame
import time
import os
from music21 import converter, meter, stream


class ImproviseAssistant:
	def __init__(self, song_file, width=500, height=200):
		self.song_file = song_file
		self.mxml_file = song_file.replace(".mp3", ".musicxml")
		self.output_folder = "assets/" + song_file.replace(".mp3", "_measures_png")
		os.makedirs(self.output_folder, exist_ok=True)

		self.bpm = 0
		self.beats_per_measure = 0
		
		self.score = converter.parse(self.mxml_file)

		for i in self.score:
			if "part" in str(i).lower():
				for p in i:
					if "measure" in str(p).lower():
						for m in p:
							if "tempo" in str(m):
								self.bpm = int(m.number)
							if "meter" in str(m):
								self.beats_per_measure = m.ratioString.split("/")[0]
								self.beat_length = m.ratioString.split("/")[1]
		
		self.seconds_per_beat = 60 / self.bpm
		self.star_time = None
		self.running = True

		pygame.init()
		pygame.mixer.init()
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("ImproviseAssistant")
		self.font = pygame.font.Font(None, 60)
