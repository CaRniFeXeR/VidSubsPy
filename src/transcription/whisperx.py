from cfgparser import ConfigParser
from pathlib import Path
import whisperx
import gc 
import torch

from src.datastructures.transcript import Transcript

class WhisperXTranscriber:

    def __init__(self, device : str ="cuda", compute_type : str = "float16") -> None:
        self.device = device
        self.compute_type = compute_type
        self.parser = ConfigParser()
    
    def transcripe_audio(self, audio_file : Path, batch_size : int = 8) -> Transcript:
        model = whisperx.load_model("medium.en", self.device, compute_type=self.compute_type)

        audio = whisperx.load_audio(audio_file)
        result = model.transcribe(audio, batch_size=batch_size)

        gc.collect(); torch.cuda.empty_cache(); del model


        aligned_segments = self._align_text_audio(audio, result["segments"], result["language"])

        transcript = self.parser.parse_typed({"segments" : aligned_segments}, Transcript)

        return transcript


    def _align_text_audio(self, audio, segments : dict, lang : str) -> dict:
        model_a, metadata = whisperx.load_align_model(language_code=lang, device=self.device)
        result = whisperx.align(segments, model_a, metadata, audio, self.device, return_char_alignments=False)

        # print(segments) # after alignment

        # delete model if low on GPU resources
        gc.collect(); torch.cuda.empty_cache(); del model_a

        return result["segments"]
