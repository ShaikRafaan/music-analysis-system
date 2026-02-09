from pydantic import BaseModel
from typing import List, Optional


class ContentSettings(BaseModel):
    enabled: bool
    locked: bool


class ProfileImage(BaseModel):
    url: str
    height: int
    width: int


class UserProfile(BaseModel):
    """
    Mapping: Spotify response -> API response

    - country: str -> country_code: str
    - display_name: str -> name: str
    - email: str -> email: str
    - explicit_content: { filter_enabled: bool, filter_locked: bool } -> content_settings: ContentSettings(enabled: bool, locked: bool)
    - external_urls: { spotify: str } -> player_url: str (Spotify URL object, used to open a user's Spotify client)
    - followers: { href: string, total: int } -> follower_count: int (documentation notes href is always set to null)
    - href: str -> web_api: str (a link to the Web API endpoint for this user)
    - id: str -> spotify_id: str (Spotify user ID object, unique string identifying the user, also found at the end of the user's Spotify URI)
    - images: [{ url: str, height: int, width: int }] -> profile_images: [ProfileImage(url: str, height: int, width: int)] (nullable list of a user's profile image, generally 300x300 and 64x64)
    - product: str -> premium: bool (the users subscription, free/premium maps to false/true)
    - uri: str -> user_uri: str (Spotify URI object for the user, resource identifier for the user, can be used to navigate to a users profile on the desktop client)

    Spotify docs: 
    - https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile
    - https://developer.spotify.com/documentation/web-api/concepts/spotify-uris-ids
    """
    country_code: str
    name: str
    email: str
    content_settings: ContentSettings
    player_url: str
    follower_count: int
    web_api: str
    spotify_id: str
    profile_images: Optional[List[ProfileImage]] = None
    premium: bool
    user_uri: str

class external_urls(BaseModel):
    spotify: str

class restrictions(BaseModel):
    reason: str


class Followers(BaseModel):
    href: Optional[str] = None
    total: int

class Album(BaseModel):
    album_type: str
    total_tracks: int
    available_markets: List[str]
    external_urls: external_urls
    href: str
    id: str
    images: List[ProfileImage]
    name: str
    release_date: str
    release_date_precision: str
    restrictions: restrictions
    type: str
    uri: str

class Artist(BaseModel):
    external_urls: external_urls
    href: str
    id: str
    name: str
    type: str
    uri: str



class ArtistObjects(BaseModel):
    """
    Artist Object fields:
    -external_urls: { spotify: str } -> web_api: str (Spotify URL object, used to open an artist's Spotify page)
    -followers: { href: string, total: int } -> follower_count: int (documentation notes href is always set to null) (Deprecated in favor of the followers.total field, which is the number of followers the artist has)
    -genres: [str] -> genres: [str] (a list of the genres the artist is associated with)(Deprecated)
    -hrefs: str -> web_api: str (a link to the Web API endpoint returning the full result of the request)
    -id: str -> spotify_id: str (Spotify artist ID object, unique string identifying the artist, also found at the end of the artist's Spotify URI)
    -images: [{ url: str, height: int, width: int }] -> profile_images: [ProfileImage(url: str, height: int, width: int)] (a list of the artist's profile images, generally 640x640, 320x320, and 160x160)
    -name: str -> name: str (the name of the artist)
    -popularity: int -> popularity: int (the popularity of the artist, between 0 and 100, with 100 being the most popular)(Deprecated)
    -type: str -> type: str (the object type, "artist")
    -uri: str -> artist_uri: str (Spotify URI object for the artist, resource identifier for the artist, can be used to navigate to an artist's profile on the desktop client)
    """
    external_urls: external_urls
    followers: Followers    
    genres: List[str]
    href: str
    id: str
    images: List[ProfileImage]
    name: str
    popularity:int
    type: str
    uri: str

class TrackObjects(BaseModel):
    """
    Track Object:
    -album: { album_type: str, artists: [object], external_urls: { spotify: str }, href: str, id: str, images: [{ url: str, height: int, width: int }], name: str, release_date: str, release_date_precision: str, total_tracks: int, type: str, uri: str } -> album: { album_type: str, artists: [dict], player_url: str, web_api: str, spotify_id: str, profile_images: [ProfileImage(url: str, height: int, width: int)], name: str, release_date: str, release_date_precision: str, total_tracks: int }
    -artists: [object] -> artists: [dict] (the artists who performed the track)
    -available_markets: [str] -> available_markets: [str] (the markets in which the track is available, identified by their ISO 3166-1 alpha-2 code)(Deprecated)
    -disc_number: int -> disc_number: int (the disc number of the track, used for albums with multiple discs)
    -duration_ms: int -> duration_ms: int (the duration of the track in milliseconds)
    -explicit: bool -> explicit: bool (whether or not the track has explicit lyrics)
    -external_ids: { isrc: str } -> external_ids: { isrc: str } (International Standard Recording Code, a unique identifier for the track)(Deprecated)
    -external_urls: { spotify: str } -> player_url: str (Spotify URL object
    -hrefs: str -> web_api: str (a link to the Web API endpoint returning the full result of the request)
    -id: str -> spotify_id: str (Spotify track ID object, unique string identifying the track, also found at the end of the track's Spotify URI)
    -is_playable: bool -> is_playable: bool (whether or not the track is playable in the given market)
    -linked_from: [object] -> linked_from: Optional[dict] (the original track of a linked track, present when the track is linked from another track)(Deprecated)
    -restrictions: { reason: str } -> restrictions: Optional[dict] (the reason why the track is not available in the given market, if applicable)
    -name: str -> name: str (the name of the track)
    -popularity: int -> popularity: int (the popularity of the track, between 0 and 100, with 100 being the most popular)(Deprecated)
    -preview_url: str -> preview_url: Optional[str] (a URL to a 30 second preview of the track in MP3 format, null if not available)
    -track_number: int -> track_number: int (the track number of the track, used for albums with multiple tracks)
    -type: str -> type: str (the object type, "track")
    -uri: str -> track_uri: str (Spotify URI object for the track, resource identifier for the track, can be used to navigate to a track's profile on the desktop client)
    -is_local: bool -> is_local: bool (whether or not the track is a local file)

    """
    album : Album
    artist:List[Artist]
    available_markets: List[str]    
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: external_urls
    href: str
    id: str
    is_playable: bool
    linked_from: Optional[dict] = None
    restriction: restrictions
    name: str
    popularity: int
    preview_url: Optional[str] = None
    track_number: int
    type: str
    uri: str
    is_local: bool




class UserTopItems(BaseModel):
    """
    Mapping: Spotify response -> API response
    -href: str -> web_api: str (a link to the Web API endpoint returning the full result of the request)
    -limit: int -> limit: int (the number of items returned, between 1 and 50)
    -next: str -> next_page: Optional[str] (the URL to the next page of items, null if there is no next page)
    -offset: int -> offset: int (the index of the first item returned, used for pagination)
    -previous: str -> previous_page: Optional[str] (the URL to the previous page of items, null if there is no previous page)
    -total: int -> total: int (the total number of items available to return, used for pagination)
    -items: [object] -> items: [dict] (the list of items returned, either artists or tracks depending on the type parameter)

    Spotify docs:
    - https://developer.spotify.com/documentation/web-api/reference/get-users-top-artists-and-tracks
    """
    href: str
    limit: int
    next : Optional[str] = None
    offset: int
    previous: Optional[str] = None
    total: int
    items: List[ArtistObjects] | List[TrackObjects]
