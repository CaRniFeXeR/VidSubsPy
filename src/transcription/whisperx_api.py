from pathlib import Path
import replicate
from src.datastructures.transcript import Transcript
from cfgparser import ConfigParser
import json
import os

class WhisperXApiTranscriber:
    
    def __init__(self) -> None:
        self.parser = ConfigParser()
        assert "REPLICATE_MODEL" in os.environ, "REPLICATE_MODEL environment variable not set"
        assert "REPLICATE_API_TOKEN" in os.environ, "REPLICATE_API_TOKEN environment variable not set"
        self.replicate_model = os.environ["REPLICATE_MODEL"]
        self.replicate_down_load_url = os.environ["REPLICATE_DOWNLOAD_URL"] if "REPLICATE_DOWNLOAD_URL" in os.environ else None

    def transcripe_audio(self, audio_path : Path) -> Transcript:

        if self.replicate_down_load_url is None:
            audio = open(str(audio_path), "rb")
        else:
            audio = self.replicate_down_load_url + str(audio_path)
        output = replicate.run(
            self.replicate_model,
            input={"audio": audio,
                   "language": "en",
                   "batch_size" : 16,
                   "debug" : True,
                   "align_output" : True}
        )

        if isinstance(output,str):
            output = json.loads(output)

        transcript = self.parser.parse_typed({"segments" : output}, Transcript)

        return transcript