from pathlib import Path
import time
from src.service.auth.jwthelper import enrich_file_path
from src.service.excerpt.topicextractor import TopicExtractor
from src.datastructures.transcript import Transcript
from src.datastructures.videoinfo import TranscriptionProcessInfo, VideoInfo
from src.service.video.videoeditor import VideoEditor
from src.repository.transcript_repository import TranscriptRepository
from src.repository.videoinfo_repository import VideoInfoRepository
from src.service.transcription.whisperx_api import WhisperXApiTranscriber

import multiprocessing

from src.utils.durationhelper import get_time_str_from_seconds

class TranscriptionHandler:

    def __init__(self, video_name : str) -> None:
        self.video_name = video_name
        self.video_path = Path(enrich_file_path(f"{video_name}/video.mp4"))
        self.audio_path = self.video_path.parent / "audio.mp3"
        self.video_repo = VideoInfoRepository()

        if not self.video_path.exists():
            raise FileNotFoundError(f"Video {video_name} not found")
        with VideoEditor(self.video_path) as videoeditor:
            self.video_duration = videoeditor.get_duration()

    def _ensure_audio_exists(self):

        if not self.audio_path.exists():
            with VideoEditor(self.video_path) as videoeditor:
                videoeditor.extract_audio()

    
    def start_transcription_process(self, use_gpu : bool = False) -> VideoInfo:
        
        start_time = time.time()
        process_info = TranscriptionProcessInfo(start_time = start_time, audio_duration=self.video_duration)
        status = f"creating transcript. estimated duration {get_time_str_from_seconds(self.video_duration / 20)} - {get_time_str_from_seconds(self.video_duration / 10)}"
        video = self.video_repo.create_or_update_transcription_process(self.video_name, status=status, process_info=process_info)

        process = multiprocessing.Process(target=self.transcripe_video, args=(start_time, use_gpu))
        process.start()

        return video

    def transcripe_video(self, start_time : float, use_gpu : bool = False) -> Transcript:

        try:
            self._ensure_audio_exists()

            transcription_fn = self.transcripe_video_cuda if use_gpu else self.trancripe_video_api
            transcript = transcription_fn()

            transcript_repo = TranscriptRepository()

            transcript = transcript_repo.save_transcript(self.video_name, transcript)
            endtime = time.time()
            n_words = transcript.get_n_words()
            process_info = TranscriptionProcessInfo(
                            start_time = start_time,
                            end_time=endtime,
                            audio_duration=self.video_duration,
                            n_words=n_words,
                            transcription_duration=endtime - start_time)
            self.video_repo.create_or_update_transcription_process(self.video_name, status="transcript created", process_info=process_info)
        except Exception as e:
            print(e)
            self.video_repo.create_or_update_transcription_process(self.video_name, status="error " + str(e))
            raise e
        
        #starting topic extraction
        topicextractor = TopicExtractor(self.video_name, segment_groupsize=15)
        topics = topicextractor.extract_merge_save_topics()

        return transcript

    def transcripe_video_cuda(self) -> Transcript:
        print("Transcribing with cuda")
        from src.service.transcription.whisperx import WhisperXTranscriber
        transcriber = WhisperXTranscriber()
        transcript = transcriber.transcripe_audio(self.audio_path)

        return transcript


    def trancripe_video_api(self) -> Transcript:
        print("Transcribing via api")
        transcriber = WhisperXApiTranscriber()
        transcript = transcriber.transcripe_audio(self.audio_path)

        return transcript