from pydantic_settings import BaseSettings

class ServerSettings(BaseSettings):
    backend_host: str
    backend_port: int
    debug: bool
    cors_origins: str

    spotify_client_id: str
    spotify_redirect_uri: str

    client_uri: str

    class Config:
        env_file = ".env"
