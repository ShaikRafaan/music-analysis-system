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
