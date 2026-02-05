import time
from schema import ServerSettings
from itsdangerous import BadSignature, SignatureExpired
from dotenv import load_dotenv
from utils import decode_cookie


load_dotenv()
settings = ServerSettings()


# Invalid or expired session cookie
class InvalidSessionError(Exception):
    pass

# Access token missing or expired
class AuthenticationError(Exception):
    pass


# Helper to get encrypted cookie, decode it, and pass it to the calling API
def get_token(session_cookie: str) -> str:
    try:
        session = decode_cookie(session_cookie, max_age=settings.session_cookie_max_age)
    except (SignatureExpired, BadSignature):
        raise InvalidSessionError

    access_token = session.get("access_token")
    expires_at = session.get("expires_at", 0)

    if not access_token or int(time.time()) >= int(expires_at):
        raise AuthenticationError

    return access_token
