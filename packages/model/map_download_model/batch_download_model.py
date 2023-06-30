from typing import TypedDict, Tuple, NewType, List

from packages.enums.map_download import Mirrors
from packages.enums.search_params_in_official import *

TypeDate = NewType("TypeDate", Tuple[int, int, int])


class DownloadParamsOfficial(TypedDict):
    q: str
    c: List[ParamsC]
    m: ParamsM
    s: ParamsS
    nsfw: ParamsNsfw
    e: ParamsE
    r: ParamsR
    played: ParamsPlayed
    l: ParamsL
    g: ParamsG
    sort: ParamsSort


class DownloadParamsFilter(TypedDict):
    ar: Tuple[float, float]
    od: Tuple[float, float]
    cs: Tuple[float, float]
    hp: Tuple[float, float]
    bpm: Tuple[float, float]
    star: Tuple[float, float]
    length: Tuple[int, int]
    ranked: Tuple[TypeDate, TypeDate]
    created: Tuple[TypeDate, TypeDate]


class DownloadParams(TypedDict):
    official: DownloadParamsOfficial
    filter: DownloadParamsFilter
    count: int
    mirror: Mirrors
