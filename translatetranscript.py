import argparse
import dataclasses
import json
from src.datastructures.transcript import Transcript
from src.translation.transcripttranslator import TranscriptTranslator
from cfgparser import ConfigParser

# CLI argument parsing
parser = argparse.ArgumentParser(description='Translate transcription.')
parser.add_argument('--input_transcript', type=str, required=True, help='Source transcript file path.')
parser.add_argument('--output_transcript', type=str, required=True, help='Output transcript file path.')
parser.add_argument('--target_language', type=str, required=True, help='Target language to transcribe to.')

args = parser.parse_args()

target_language = args.target_language
input_transcript = args.input_transcript
output_transcript = args.output_transcript

translator = TranscriptTranslator(target_language)

parser = ConfigParser()
transcript = parser.parse_form_file_typed(input_transcript, Transcript)

translated_transcript = translator.translate(transcript)

with open(output_transcript, "w") as f:
    json.dump(dataclasses.asdict(transcript), f, indent=4)

