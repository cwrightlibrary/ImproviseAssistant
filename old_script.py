import os
import pygame
import time
from music21 import converter, meter, stream


class ImproviseAssistant:
	def __init__(self, song_file, width=400, height=200):
		self.song_file = song_file
		self.bpm = 0
		self.current_beat = 0
		self.beats_per_measure = 0
		self.beat_length = 0
		self.current_measure = 1
		self.current_beat_in_measure = 0

		self.mxml_file = song_file.replace(".mp3", ".musicxml")
		self.output_folder = "assets/" + song_file.replace(".mp3", "_measures_png")
		os.makedirs(self.output_folder, exist_ok=True)

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
		
		pygame.init()
		pygame.mixer.init()
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Improvise Assistant")
		self.font = pygame.font.Font(None, 80)
		self.running = True
	
	def save_measure_images(self):
		pass

	def play_song(self):
		pygame.mixer.music.load(self.song_file)
		pygame.mixer.music.play()
		self.start_time = time.time()
	
	def update_beat(self):
		elapsed_time = time.time() - self.start_time
		total_beats = int(elapsed_time / self.seconds_per_beat)

		self.current_measure = total_beats // self.beats_per_measure + 1
		self.current_beat_in_measure = total_beats % self.beats_per_measure + 1
	
	def draw(self):
		self.screen.fill((0, 0, 0))
		text_surface = self.font.render(f"Measure: {self.current_measure}  Beat: {self.current_beat_in_measure}", True, (255, 255, 255))
		text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
		self.screen.blit(text_surface, text_rect)
		pygame.display.flip()
	
	def run(self):
		self.play_song()
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					pygame.mixer.music.stop()
			
			self.update_beat()
			self.draw()
			pygame.time.delay(10)
		
		pygame.quit()


if __name__ == "__main__":
	song_file = "assets/my_one_and_only_love.mp3"
	app = ImproviseAssistant(song_file)
	app.run()