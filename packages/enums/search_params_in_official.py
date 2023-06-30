from enum import Enum


# from enum import UNIQUE


class ParamsC(Enum):
    Recommended = "recommended"
    ConvertMapIncluded = "converts"
    FollowMappers = "follows"
    SpotlightMaps = "spotlights"
    FeaturedArtists = "featured_artists"


class ParamsM(Enum):
    Std = 0
    Taiko = 1
    Catch = 2
    Mania = 3


class ParamsS(Enum):
    Any = "any"
    Ranked = "ranked"
    Qualified = "qualified"
    Loved = "loved"
    Favourites = "favourites"
    Pending = "pending"
    Wip = "wip"
    Graveyard = "graveyard"
    Mine = "mine"


class ParamsNsfw(Enum):
    Included = True
    Excluded = False


class ParamsE(Enum):
    Video = "video"
    Storyboard = "storyboard"


class ParamsR(Enum):
    XH = "XH"
    X = "X"
    SSH = "XH"
    SS = "X"
    SH = "SH"
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class ParamsPlayed(Enum):
    Played = "played"
    Unplayed = "unplayed"


class ParamsL(Enum):
    Unspecified = 1
    English = 2
    Japanese = 3
    Chinese = 4
    Instrumental = 5
    Korean = 6
    French = 7
    Germany = 8
    Swedish = 9
    Spanish = 10
    Italian = 11
    Russian = 12
    Polish = 13
    Others = 14


class ParamsG(Enum):
    Unspecified = 1
    VideoGame = 2
    Anime = 3
    Rock = 4
    Pop = 5
    Others = 6
    Novelty = 7
    HipHop = 9
    Electronic = 10
    Metal = 11
    Classical = 12
    Folk = 13
    Jazz = 14


class ParamsSort(Enum):
    Title = "title_asc"
    TitleReverse = "title_desc"
    Artist = "artist_asc"
    ArtistReverse = "artist_desc"
    Difficulty = "difficulty_asc"
    DifficultyReverse = "difficulty_desc"
    Ranked = "ranked_asc"
    RankedReverse = "ranked_desc"
    Rating = "rating_asc"
    RatingReverse = "rating_desc"
    Plays = "plays_asc"
    PlaysReverse = "plays_desc"
    Favourites = "favourites_asc"
    FavouritesReverse = "favourites_desc"
