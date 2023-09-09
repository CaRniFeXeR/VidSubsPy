from pathlib import Path
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, VideoClip
from moviepy.video.tools.subtitles import SubtitlesClip
from src.datastructures.textoverlay import TextOverlayInfo

from src.utils.logginghandler import LoggingHandler


class VideoEditor:

    def __init__(self, video_path : Path, log_id : str = "default") -> None:

        if isinstance(video_path, str):
            video_path = Path(video_path)

        if not video_path.exists():
            raise ValueError(f"given video_path '{video_path}' does not exist")

        self.video_path = video_path
        self.log_id = log_id
        self.log = LoggingHandler(self.log_id)
        

    def __enter__(self):
        self.video = VideoFileClip(str(self.video_path))
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.video.close()

    def get_duration(self) -> float:

        return self.video.duration

    def extract_audio(self) -> Path:

        output_path = self.video_path.parent / Path(self.video_path.stem + ".mp3")
        audio = self.video.audio.set_fps(16000)
        audio.write_audiofile(str(output_path),
                              codec="mp3",
                              ffmpeg_params=["-ac", "1"],
                              verbose=False,
                              logger=None,
                              fps=16000) # ["-ac", "1"] -> sets mono channel

        self.log.info(f"sucessfully extracted audio to {output_path}")
        audio.close()

        return output_path

    def add_transcript(self, video, overlayinfo : TextOverlayInfo):
        self.log.debug(f"adding transcript to video")
        self.log.debug(f"overlayinfo: {overlayinfo.position} {overlayinfo.size} {overlayinfo.color}")
        if video is None:
            video = self.video
        video_size = video.size

        def gen_text_clip(txt):
                txt_clip = TextClip(txt, fontsize=overlayinfo.size, color=overlayinfo.color, font= overlayinfo.font, bg_color="#ffffff60")
                return txt_clip

        subs = [((ol.start, ol.end), ol.text) for ol in overlayinfo.overlays]

        subtitles = SubtitlesClip(subs, gen_text_clip)

        if overlayinfo.position != None:
            subtitles = subtitles.set_position(("center", overlayinfo.position[1] / video_size[1]), relative=True)
        else:
            subtitles = subtitles.set_position(("center", 0.70), relative=True)

        final_clip = CompositeVideoClip([video, subtitles])
    

        return final_clip

    def write_video(self, video : VideoClip, output_path : Path):
        self.log.info(f"start writing video to {output_path}")
        video.write_videofile(str(output_path), threads = 6, verbose=False, logger=None, fps = 24, codec="libx264" , ffmpeg_params=["-pix_fmt", "yuv420p"])
        self.log.info(f"sucessfully saved video to {output_path}")
        video.close()

    def get_duration(self):

        return self.video.duration