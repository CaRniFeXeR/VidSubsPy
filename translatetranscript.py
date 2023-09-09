import dataclasses
import json
from src.datastructures.transcript import Transcript
from src.translation.transcripttranslator import TranscriptTranslator
from cfgparser import ConfigParser

INPUT_TRANSCRIPT_FILEPATH = "my_transcript.json"
OUTPUT_TRANSCRIPT_FILEPATH = "transcript.json"

TARGET_LANGUAGE = "vietnamese"

translator = TranscriptTranslator(TARGET_LANGUAGE)

parser = ConfigParser()
transcript = parser.parse_form_file_typed(INPUT_TRANSCRIPT_FILEPATH, Transcript)

translated_transcript = translator.translate(transcript)

with open(OUTPUT_TRANSCRIPT_FILEPATH, "w") as f:
    json.dump(dataclasses.asdict(transcript), f, indent=4)

