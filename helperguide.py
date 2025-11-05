from music21 import converter, environment

env = environment.UserSettings()
# env["musicxmlPath"] = /Applications/MuseScore 3.app/Contents/MacOS/mscore
env["musicxmlPath"] = "/Applications/MuseScore 4.app/Contents/MacOS/mscore"
print(env["musicxmlPath"])

score = converter.parse("assets/my_one_and_only_love.musicxml")
score.write("musicxml.png", fp="test.png")