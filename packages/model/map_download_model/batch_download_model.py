from typing import TypedDict, Tuple

from packages.enums.map_download import Mirrors
from packages.model.osu_web.beatmap import BeatmapParamsOfficial


class DownloadParamsFilter(TypedDict):
    ar: Tuple[float, float]
    od: Tuple[float, float]
    cs: Tuple[float, float]
    hp: Tuple[float, float]
    bpm: Tuple[float, float]
    star: Tuple[float, float]
    length: Tuple[float, float]
    ranked: Tuple[Tuple[int, int, int], Tuple[int, int, int]]
    created: Tuple[Tuple[int, int, int], Tuple[int, int, int]]


class DownloadParams(TypedDict):
    official: BeatmapParamsOfficial
    filter: DownloadParamsFilter
    count: int
    mirror: Mirrors
