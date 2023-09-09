from dataclasses import dataclass
from typing import List, Tuple

from src.datastructures.transcript import Word

@dataclass
class TextOverlay:
    start : float
    end : float
    text : str



@dataclass
class TextOverlayInfo:
    position : Tuple[float, float] = None
    size : int = 30
    color : str = "black"
    font : str = "Arial"
    overlays : List[TextOverlay] = None