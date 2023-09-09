
import dataclasses
import json
from pathlib import Path
from src.video.videoeditor import VideoEditor
from src.transcription.whisperx_api import WhisperXApiTranscriber


INTPUT_VIDEO_FILEPATH = "pf_learn_clip.mp4"
OUTPUT_TRANSCRIPT_FILEPATH = "transcript.json"
audio_filepath = None
with VideoEditor(Path(INTPUT_VIDEO_FILEPATH)) as editor:
   audio_filepath = editor.extract_audio()

wt = WhisperXApiTranscriber()
transcript = wt.transcripe_audio(audio_filepath)

with open(OUTPUT_TRANSCRIPT_FILEPATH, "w") as f:
    json.dump(dataclasses.asdict(transcript), f, indent=4)