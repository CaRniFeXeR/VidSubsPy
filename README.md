# VidSubsPy
automated video subtitles creation using whisperx, moviepy and optional chatGPT for translation


## Overview

This Python library provides a comprehensive solution for generating subtitles for videos in different languages. It leverages:

- **WhisperX ASR** for speech-to-text transcription.
- **ChatGPT** for optional translation of the transcription.
- **MoviePy** for generating videos with subtitles.

## Core Functionalities

### 1. Video to Transcript (`vid2transcript.py`)

This script converts a given video file into a transcript file (json). It uses WhisperX ASR for the transcription process.

#### Usage:

```bash
python vid2transcript.py --input_video /path/to/video.mp4 --output_transcript /path/to/transcript.json
```

### 2. Translate Transcript (`translatetranscript.py`)

This script translates an existing transcript file into another language. The translation is done using ChatGPT.

#### Usage:

```bash
python translatetranscript.py --input_transcript /path/to/transcript.json --output_transcript /path/to/translated_transcript.json --target_language es
```

### 3. Transcript to Subtitled Video (`transcript2subvid.py`)

This script takes a transcript file and an original video to generate a new video with subtitles. The subtitles are generated using the MoviePy library.

#### Usage:

```bash
python transcript2subvid.py --input_transcript /path/to/transcript.json --input_video /path/to/video.mp4 --output_video /path/to/video_with_subtitles.mp4
```

## Installation

```bash
pip install -r requirements.txt
```

## Dependencies

- Whisper X ASR
- ChatGPT (Optional for translation)
- MoviePy

