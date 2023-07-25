from typing import TypedDict, List, Optional

from packages.enums.search_params_in_official import *


class BeatmapParamsOfficial(TypedDict):
    q: str
    c: List[ParamsC]
    m: ParamsM
    s: ParamsS
    nsfw: ParamsNsfw
    e: List[ParamsE]
    r: List[ParamsR]
    played: ParamsPlayed
    l: ParamsL
    g: ParamsG
    sort: ParamsSort
    cursor_string: Optional[str]
