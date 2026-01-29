from pydantic_settings import BaseSettings

class ServerSettings(BaseSettings):
    backend_host: str
    backend_port: int
    debug: bool
    cors_origins: str

    class Config:
        env_file = ".env"
