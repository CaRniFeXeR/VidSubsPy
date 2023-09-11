import argparse
from cfgparser import ConfigParser
from src.datastructures.textoverlay import TextOverlayInfo
from src.datastructures.transcript import Transcript
from src.video.subtitlehandler import SubtitleHandler


# CLI argument parsing
parser = argparse.ArgumentParser(description='Generate subtitles for a video.')
parser.add_argument('--input_video', type=str, required=True, help='Input video file path.')
parser.add_argument('--input_transcript', type=str, required=True, help='Input transcript file path.')
parser.add_argument('--output_video', type=str, required=True, help='Output video file path.')
parser.add_argument('--size', type=int, default=35, help='Font size for subtitles.')
parser.add_argument('--color', type=str, default="black", help='Font color for subtitles.')
parser.add_argument('--font', type=str, default="Arial", help='Font type for subtitles.')
parser.add_argument('--max_word_per_line', type=int, default=5, help='Maximum number of words per line in subtitles.')

args = parser.parse_args()

# Assign CLI arguments to variables
input_video_filepath = args.input_video
input_transcript_filepath = args.input_transcript
output_video_filepath = args.output_video
size = args.size
color = args.color
font = args.font
max_word_per_line = args.max_word_per_line



parser = ConfigParser()
transcript = parser.parse_form_file_typed(input_transcript_filepath, Transcript)

overlayinfo = TextOverlayInfo(size=size, color=color, font=font)

subhandler = SubtitleHandler(max_word_per_line=5)
subhandler.imprint_subtitles(transcript, overlayinfo, input_video_filepath, output_video_filepath)