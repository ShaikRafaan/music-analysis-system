from pydantic import BaseModel


class CookieConfig(BaseModel):
    secure: bool
    samesite: str
