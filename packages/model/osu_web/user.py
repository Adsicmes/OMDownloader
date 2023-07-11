from typing import List, TypedDict

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


class UserModel(TypedDict):
    avatar_url: str
    blocks: list
    country: _Country
    country_code: str
    cover: _Cover
    cover_url: str
    default_group: str
    discord: str
    follow_user_mapping: list
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
    join_date: int
    kudosu: _Kudosu
    last_visit: int
    location: str
    max_blocks: str
    max_friends: int
    occupation: str
    playmode: PlayMode
    playstyle: List[str]
    pm_friends_only: bool
    post_count: int
    profile_colour: str
    profile_order: List[str]
    title: str
    title_url: str
    twitter: str
    unread_pm_count: int
    user_preferences: _UserPreferences
    username: str
    website: str
