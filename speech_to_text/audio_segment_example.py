from pydub import AudioSegment

file_location = "/home/varun/Downloads/david.mp3"
sound = AudioSegment.from_mp3(file_location)
# should have ffmpeg installed
# sudo apt-get install ffpmeg