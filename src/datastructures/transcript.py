from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Word:
    word : str
    start : Optional[float] = None
    end : Optional[float] = None
    score : Optional[float] = None


@dataclass
class Segment:
    start : float
    end : float
    text : str
    words : List[Word]


@dataclass
class Transcript:
    segments : List[Segment] = None
    duration_label : str = None

    def get_n_words(self) -> int:
        return sum([len(segment.words) for segment in self.segments])

    def get_all_words(self) -> List[Word]:
        words = []
        for segment in self.segments:
            words.extend(segment.words)
        return words
    
    def get_all_words_text(self) -> List[str]:
        words = []
        for segment in self.segments:
            for word in segment.words:
                words.append(word.word)
        return  words
    
    def get_text_by_segment(self) -> List[str]:
        return [segment.text for segment in self.segments]
    
    def get_avg_segment_duration(self) -> float:
        return (self.segments[-1].end - self.segments[0].start) / len(self.segments)
