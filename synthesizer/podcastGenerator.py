import os
from TTS.utils.synthesizer import Synthesizer
from pathlib import Path, PureWindowsPath
from typing import Dict
import time
import json
import torch

from flask import Flask, request

app = Flask(__name__)

@app.route('/generatePodcast', methods=['POST'])
def process_data():
    data = request.get_json()

    if 'reader' in data and 'language' in data and 'text' in data:
        reader = data['reader']
        language = data['language']
        text = data['text']

        output_dir = output_input.get()
        voice = reader
        synthesize(text, voice, output_dir)

        print("Reader:", reader)
        print("Language:", language)
        print("Text:", text)

        return "Data processed successfully."
    else:
        return "Invalid data format."

if __name__ == '__main__':
    app.run()

base_model_path = Path(PureWindowsPath(".\\models\\"))
config_path = base_model_path / "config.json"
output_path = Path(PureWindowsPath(".\\output\\"))
sample_rate = 22050
synthesizers: Dict[str, Synthesizer] = {}
voices = {}
with open("models.json", "r") as f:
    models = json.load(f)
    for voice in models["voices"]:
        voices[voice["name"]] = voice

def synthesize(text: str, voice: str, output_dir: str):
    global synthesizer

    if not os.path.exists(output_dir):
        print("Error", "Output directory does not exist.")
        return

    model_file = base_model_path / voices[voice]["model"]
    if not os.path.exists(model_file):
        print("Error", f"Model file {voices[voice]['model']} does not exist.")
        return

    if not os.path.exists(config_path):
        print("Error", f"Config file {config_path} does not exist.")
        return

    print(voices[voice]["model"])
    if voice not in synthesizers:
        synthesizers[voice] = Synthesizer(
            tts_config_path=config_path,
            tts_checkpoint=model_file,
        )
    wav = synthesizers[voice].tts(text)

    output_filename = f"{int(time.time())}_{voice}.wav"
    path = os.path.join(output_dir, output_filename)
    synthesizers[voice].save_wav(wav, path)
