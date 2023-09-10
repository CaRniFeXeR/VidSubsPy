from pathlib import Path
from typing import List
from src.datastructures.textoverlay import TextOverlay, TextOverlayInfo
from src.datastructures.transcript import Transcript
from src.video.videoeditor import VideoEditor


class SubtitleHandler:

    def __init__(self, max_word_per_line : int, new_line_symbols : List[str] = [".", "?", "!", ","]) -> None:
        self.max_word_per_line = max_word_per_line
        self.new_line_symbols = new_line_symbols

    def imprint_subtitles(self, transcript : Transcript, overlay_info : TextOverlayInfo, video_path : str, output_path : str):
        
        overlay_info.overlays = self.create_subtitles_from_transcript(transcript)
        
        with VideoEditor(Path(video_path)) as editor:
            transcript_video = editor.add_transcript(editor.video, overlay_info)
            editor.write_video(transcript_video, Path(output_path))

    def _new_line_symbol_in_word(self, word : str) -> bool:
        for symbol in self.new_line_symbols:
            if symbol in word:
                return True
        return False

    def create_subtitles_from_transcript(self, transcript : Transcript):
        overlays = []

        for segment in transcript.segments:
            overlay = TextOverlay(segment.start, segment.end,"")
            words = segment.text.split(" ")
            word_line_count = 0
            for word in words:
                word_line_count += 1
                overlay.text += word + " "
                if word_line_count >= self.max_word_per_line or self._new_line_symbol_in_word(word):
                    overlay.text += "\n"
                    word_line_count = 0
        
            overlays.append(overlay)
        
        return overlays
