from music21 import converter, stream, environment
import os

# Set up the MuseScore path in music21 environment
env = environment.UserSettings()
env['musicxmlPath'] = '/usr/bin/musescore3'  # adjust to your MuseScore executable
env['musescoreDirectPNGPath'] = '/usr/bin/musescore3'

# Load your score
score = converter.parse("path_to_your_file.musicxml")

# Create an output folder
output_folder = "measures_png"
os.makedirs(output_folder, exist_ok=True)

# Iterate through measures
for i, measure in enumerate(score.parts[0].getElementsByClass(stream.Measure), start=1):
    # Create a new single-measure score
    measure_score = stream.Score()
    part = stream.Part()
    part.append(measure)
    measure_score.append(part)
    
    # Save the measure as a MusicXML file first
    xml_path = os.path.join(output_folder, f"measure_{i}.musicxml")
    measure_score.write('musicxml', fp=xml_path)
    
    # Convert MusicXML to PNG using MuseScore
    png_path = os.path.join(output_folder, f"measure_{i}.png")
    measure_score.write('musicxml.png', fp=png_path)  # music21 uses MuseScore for PNG export

print("Done! Each measure saved as a PNG.")




import pygame
import time

class MeasureTracker:
    def __init__(self, song_file, bpm, beats_per_measure, width=500, height=200):
        self.song_file = song_file
        self.bpm = bpm
        self.beats_per_measure = beats_per_measure

        self.seconds_per_beat = 60 / self.bpm

        self.start_time = None
        self.running = True

        # Pygame setup
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Measure Tracker")
        self.font = pygame.font.Font(None, 60)

    def play_song(self):
        pygame.mixer.music.load(self.song_file)
        pygame.mixer.music.play()
        self.start_time = time.time()

    def get_current_measure_and_beat(self):
        """Return current measure and beat based on elapsed time"""
        elapsed_time = time.time() - self.start_time
        total_beats = int(elapsed_time / self.seconds_per_beat)
        current_measure = total_beats // self.beats_per_measure + 1
        current_beat_in_measure = total_beats % self.beats_per_measure + 1
        return current_measure, current_beat_in_measure

    def draw(self, measure, beat):
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
    song_file = "song.mp3"  # replace with your file
    bpm = 120
    beats_per_measure = 4  # e.g., 4/4 time

    tracker = MeasureTracker(song_file, bpm, beats_per_measure)
    tracker.run()
