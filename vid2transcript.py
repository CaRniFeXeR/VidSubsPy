
import argparse
import dataclasses
import json
from pathlib import Path
from src.video.videoeditor import VideoEditor
from src.transcription.whisperx_api import WhisperXApiTranscriber

parser = argparse.ArgumentParser(description='Transcribe video.')
parser.add_argument('--input_video', type=str, required=True, help='Input video file path.')
parser.add_argument('--output_transcript', type=str, required=True, help='Output transcript file path.')


args = parser.parse_args()

input_video = args.input_video
output_transcript = args.output_transcript

audio_filepath = None
with VideoEditor(Path(input_video)) as editor:
   audio_filepath = editor.extract_audio()

wt = WhisperXApiTranscriber()
transcript = wt.transcripe_audio(audio_filepath)

with open(output_transcript, "w") as f:
    json.dump(dataclasses.asdict(transcript), f, indent=4)