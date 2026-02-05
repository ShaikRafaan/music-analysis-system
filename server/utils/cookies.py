from itsdangerous import URLSafeTimedSerializer
from fastapi.responses import RedirectResponse
from schema import ServerSettings, CookieConfig
from dotenv import load_dotenv

load_dotenv()
settings = ServerSettings()


# Helper for setting cookies, checks debug mode and configures secure and samesite settings for dev/prod
def _cookie_config() -> CookieConfig:
    if settings.debug:
        secure = False
        samesite = "lax"
    else:
        secure = True
        samesite = "none"

    return CookieConfig(
        secure=secure,
        samesite=samesite
    )


# Used to set HttpOnly cookie with auth tokens 
def set_cookie(response: RedirectResponse, key: str, value: str, age: int) -> None:
    config = _cookie_config()    
    response.set_cookie(
        key=key,
        value=value,
        httponly=True,
        secure=config.secure,
        samesite=config.samesite,
        max_age=age,
        path="/",
    )


# Delete cookies with expired auth tokens before refresh
def delete_cookie(response: RedirectResponse, key: str) -> None:
    config = _cookie_config()
    response.delete_cookie(
        key=key,
        path="/",
        secure=config.secure,
        samesite=config.samesite,
    )


# Encode/decode cookie before setting
serializer = URLSafeTimedSerializer(settings.cookie_secret, salt=settings.cookie_salt)

def encode_cookie(cookie: dict) -> str:
    return serializer.dumps(cookie)

def decode_cookie(token: str, max_age: int) -> dict:
    return serializer.loads(token, max_age=max_age)
