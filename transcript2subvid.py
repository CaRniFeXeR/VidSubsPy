from cfgparser import ConfigParser
from src.datastructures.textoverlay import TextOverlayInfo
from src.datastructures.transcript import Transcript
from src.video.subtitlehandler import SubtitleHandler


INTPUT_VIDEO_FILEPATH = "my_video.mp4"
INPUT_TRANSCRIPT_FILEPATH = "my_transcript.json"

OUTPUT_VIDEO_FILEPATH = "my_video_with_subs.mp4"

subhandler = SubtitleHandler(max_word_per_line=5)

parser = ConfigParser()
transcript = parser.parse_form_file_typed("pf_transcript.json", Transcript)

overlayinfo = TextOverlayInfo(size=35, color="black", font="Arial")
subhandler.imprint_subtitles(transcript, overlayinfo, INTPUT_VIDEO_FILEPATH, OUTPUT_VIDEO_FILEPATH)