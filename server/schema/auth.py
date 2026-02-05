from pydantic import BaseModel
from typing import Optional


class CookieConfig(BaseModel):
    secure: bool
    samesite: str


class PKCECookie(BaseModel):
    state: str
    code_verifier: str


class StatusResponse(BaseModel):
    authenticated: bool


class SpotifyTokenResponse(BaseModel):
    access_token: str
    token_type: str
    scope: str
    expires_in: int
    refresh_token: Optional[str] = None
