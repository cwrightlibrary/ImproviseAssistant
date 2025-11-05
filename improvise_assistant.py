import pygame
import time
import os
from music21 import converter, stream, harmony


class ImproviseAssistant:
	def __init__(self, song_file, width=500, height=200):
		self.song_file = song_file
		self.mxml_file = song_file.replace(".mp3", ".musicxml")

		self.output_folder = "assets/" + song_file.replace(".mp3", "_measures_png")
		os.makedirs(self.output_folder, exist_ok=True)

		self.bpm = 0
		self.beats_per_measure = 0
		
		self.score = converter.parse(self.mxml_file)
		self.save_all_measure_images()

		for i in self.score:
			if "part" in str(i).lower():
				for p in i:
					if "measure" in str(p).lower():
						for m in p:
							if "tempo" in str(m):
								self.bpm = int(m.number)
							if "meter" in str(m):
								self.beats_per_measure = int(m.ratioString.split("/")[0])
								self.beat_length = int(m.ratioString.split("/")[1])
		
		self.seconds_per_beat = 60 / self.bpm
		self.star_time = None
		self.running = True

		pygame.init()
		pygame.mixer.init()
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption("ImproviseAssistant")
		self.font = pygame.font.Font(None, 60)

		self.measure_images = {}
	
	def save_all_measure_images(self):
		existing_pngs = [f for f in os.listdir(self.output_folder) if f.endswith(".png")]
		if existing_pngs:
			return
		
		expanded_score = self.score.expandRepeats()
		part = expanded_score.parts[0] # type: ignore

		chords = part.recurse().getElementsByClass(harmony.ChordSymbol)

		for i, measure in enumerate(part.getElementsByClass(stream.Measure), start=1):
			measure_score = stream.Score()
			single_part = stream.Part()

			measure_copy = measure.flat
			single_part.append(measure)

			measure_offset = measure.offset
			measure_length = measure.quarterLength

			for c in chords:
				if measure_offset <= c.offset < measure_offset + measure_length:
					c_copy = c
					c_copy.offset -= measure_offset
					single_part.insert(c_copy.offset, c_copy)

			measure_score.append(single_part)

			base_path = os.path.join(self.output_folder, f"measure_{i:03}")
			xml_path = base_path + ".musicxml"
			png_path = base_path + ".png"

			measure_score.write("musicxml.png", fp=png_path)
			if os.path.exists(xml_path):
				os.remove(xml_path)
	
	def play_song(self):
		pygame.mixer.music.load(self.song_file)
		pygame.mixer.music.play()
		self.start_time = time.time()

	def get_current_measure_and_beat(self):
		elapsed_time = time.time() - self.start_time
		total_beats = int(elapsed_time / self.seconds_per_beat)
		current_measure = total_beats // self.beats_per_measure + 1
		current_beat_in_measure = total_beats % self.beats_per_measure + 1
		return current_measure, current_beat_in_measure

	def draw(self, measure, beat):
		self.screen.fill((255, 255, 255))

		if measure not in self.measure_images:
			img_path = os.path.join(self.output_folder, f"measure_{measure:03}-1.png")
			if os.path.exists(img_path):
				img = pygame.image.load(img_path).convert_alpha()
				self.measure_images[measure] = img
			else:
				self.measure_images[measure] = None
		
		img = self.measure_images[measure]

		if img:
			img_rect = img.get_rect()
			scale_factor = self.screen.get_width() / img_rect.width
			new_height = int(img_rect.height * scale_factor)
			img = pygame.transform.smoothscale(img, (self.screen.get_width(), new_height))

			img_rect = img.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
			self.screen.blit(img, img_rect)
		else:
			text_surface = self.font.render(f"Measure {measure}", True, (0, 0, 0))
			text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
			self.screen.blit(text_surface, text_rect)
		
		pygame.display.flip()

	def old_draw(self, measure, beat):
		self.screen.fill((0, 0, 0))
		text_surface = self.font.render(f"Measure: {measure}  Beat: {beat}", True, (255, 255, 255))
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
			
			measure, beat = self.get_current_measure_and_beat()
			self.draw(measure, beat)
			pygame.time.delay(10)
		
		pygame.quit()


if __name__ == "__main__":
	song_file = "assets/my_one_and_only_love.mp3"
	app = ImproviseAssistant(song_file)
	app.run()
