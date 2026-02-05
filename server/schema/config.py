from pydantic_settings import BaseSettings

class ServerSettings(BaseSettings):
    backend_host: str
    backend_port: int
    debug: bool
    cors_origins: str
    client_uri: str

    spotify_auth_url: str
    spotify_token_url: str
    spotify_client_id: str
    spotify_redirect_uri: str
    spotify_token_scopes: str

    cookie_secret: str
    cookie_salt: str
    pkce_cookie: str
    session_cookie: str
    pkce_cookie_max_age: int
    session_cookie_max_age: int

    class Config:
        env_file = ".env"
