from datetime import datetime
from typing import List, TypedDict, Any, Union

from packages.enums import PlayMode


class _Country(TypedDict):
    code: str
    name: str


class _Cover(TypedDict):
    custom_url: str
    id: int
    url: str


class _Friend(TypedDict):
    mutual: bool
    relation_type: str
    target_id: int


class _Kudosu(TypedDict):
    total: int
    available: int


class _UserPreferences(TypedDict):
    audio_autoplay: bool
    audio_muted: bool
    audio_volume: float
    beatmapset_card_size: str
    beatmapset_download: str
    beatmapset_show_nsfw: bool
    beatmapset_title_show_original: bool
    comments_show_deleted: bool
    forum_posts_show_deleted: bool
    profile_cover_expanded: bool
    user_list_filter: str
    user_list_sort: str
    user_list_view: str


class _UserBadge(TypedDict):
    awarded_at: int
    description: str
    image_url: str
    url: str


class _RankHighest(TypedDict):
    rank: int
    updated_at: Union[str, datetime]


class _Level(TypedDict):
    level: int
    progress: int


class _Rank(TypedDict):
    rank: int


class _GradeCounts(TypedDict):
    ss: int
    ssh: int
    s: int
    sh: int
    a: int


class _Statistics(TypedDict):
    count_100: int
    count_300: int
    count_50: int
    count_miss: int
    level: _Level
    global_rank: int
    global_rank_exp: int
    pp: float
    pp_exp: float
    rank_score: int
    hit_accuracy: float
    play_count: int
    play_time: int
    total_score: int
    total_hits: int
    maximum_combo: int
    replays_watched_by_others: int
    is_ranked: bool
    grade_counts: _GradeCounts
    country_rank: int
    rank: _Rank


class LoginUserModel(TypedDict):
    avatar_url: str
    account_history: list
    active_tournament_banner: Any
    badges: List[_UserBadge]
    blocks: list
    comments_count: int
    country: _Country
    country_code: str
    cover: _Cover
    cover_url: str
    default_group: str
    discord: str
    follow_user_mapping: list
    follower_count: int
    friends: List[_Friend]
    groups: list
    has_supported: bool
    id: int
    interests: str
    is_active: bool
    is_admin: bool
    is_bng: bool
    is_bot: bool
    is_deleted: bool
    is_full_bn: bool
    is_gmt: bool
    is_limited_bn: bool
    is_moderator: bool
    is_nat: bool
    is_online: bool
    is_restricted: bool
    is_silenced: bool
    is_supporter: bool
    join_date: Union[str, datetime]
    kudosu: _Kudosu
    last_visit: Union[str, datetime]
    location: str
    max_blocks: str
    max_friends: int
    mapping_follower_count: int
    occupation: str
    pending_beatmapset_count: int
    playmode: PlayMode
    playstyle: List[str]
    pm_friends_only: bool
    post_count: int
    previous_usernames: List[str]
    profile_colour: str
    profile_order: List[str]
    rank_highest: _RankHighest
    statistics: _Statistics
    title: str
    title_url: str
    twitter: str
    unread_pm_count: int
    user_preferences: _UserPreferences
    username: str
    website: str
