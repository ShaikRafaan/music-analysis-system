import time
import secrets
import httpx
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from schema import ServerSettings, StatusResponse, PKCECookie, SpotifyTokenResponse
from itsdangerous import BadSignature, SignatureExpired
from urllib.parse import urlencode
from dotenv import load_dotenv
from utils import get_pkce, encode_cookie, decode_cookie, set_cookie, delete_cookie


load_dotenv()
settings = ServerSettings()
router = APIRouter(prefix="/auth")


@router.get("/login")
async def login() -> RedirectResponse:
    """
    Sets the PKCE values as a HttpOnly cookie and redirects to spotify
    """

    code_verifier, code_challenge = get_pkce()
    state = secrets.token_urlsafe(32)

    pkce_cookie_value = encode_cookie({
        "state": state,
        "code_verifier": code_verifier
    })

    params = {
        "client_id": settings.spotify_client_id,
        "response_type": "code",
        "redirect_uri": settings.spotify_redirect_uri,
        "state": state,
        "scope": settings.spotify_token_scopes,  
        "code_challenge_method": "S256",
        "code_challenge": code_challenge,
    }

    auth_url = f"{settings.spotify_auth_url}?{urlencode(params)}"
    response = RedirectResponse(
        url=auth_url,
        status_code=302
    )

    try:
        set_cookie(
            response,
            settings.pkce_cookie,
            pkce_cookie_value,
            settings.pkce_cookie_max_age
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error setting PKCE cookie: {str(e)}")

    return response


@router.get("/callback")
async def callback(request: Request):
    """
    Spotify redirects to this endpoint with url params ?code=...&state=...
    Validates state, exchanges code, receives access and refresh tokens, sets session cookie, and then redirects to frontend.
    """
    # TODO: Ensure we are redirected to the frontend regardless of accepted/rejected permissions
    # KNOWN BUG: User cancelling Spotify's auth leads to redirect to backend page and raw json stating "authorization: declined"

    params = dict(request.query_params)
    if "error" in params:
        error = params.get("error")
        raise HTTPException(status_code=400, detail=f"Error from Spotify Auth: {error}")

    code = params.get("code")
    returned_state = params.get("state")
    if not code or not returned_state:
        raise HTTPException(status_code=400, detail="Missing code or state in callback")

    pkce_cookie = request.cookies.get(settings.pkce_cookie)
    if not pkce_cookie:
        raise HTTPException(status_code=400, detail="Missing PKCE cookie or login session expired")

    try:
        pkce_data = decode_cookie(pkce_cookie, max_age=settings.pkce_cookie_max_age)
        pkce = PKCECookie(**pkce_data)
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="PKCE cookie expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid PKCE cookie")
    except Exception:
        raise HTTPException(status_code=400, detail="Malformed PKCE cookie")

    if pkce.state != returned_state:
        raise HTTPException(status_code=400, detail="State mismatch, possible CSRF attempt")
    
    data = {
        "client_id": settings.spotify_client_id,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.spotify_redirect_uri,
        "code_verifier": pkce.code_verifier,
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    token_payload = {}
    async with httpx.AsyncClient(timeout=20) as client:
        res = await client.post(settings.spotify_token_url, data=data, headers=headers)
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Spotify token exchange failed: {res.text}")

        payload = res.json()
        token_payload = SpotifyTokenResponse(**payload)

    if not token_payload:
        raise HTTPException(status_code=400, detail="No payload received from Spotify")

    now = int(time.time())
    session_obj = {
        "access_token": token_payload.access_token,
        "refresh_token": token_payload.refresh_token,
        "scope": token_payload.scope,
        "token_type": token_payload.token_type,
        "expires_at": now + int(token_payload.expires_in),
    }
    session_cookie_value = encode_cookie(session_obj)

    redirect_to = f"{settings.client_uri}/"
    response = RedirectResponse(url=redirect_to, status_code=302)

    delete_cookie(response, settings.pkce_cookie)

    try:
        set_cookie(
            response,
            settings.session_cookie,
            session_cookie_value,
            settings.session_cookie_max_age
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error setting session cookie: {str(e)}")

    return response


@router.get("/status", response_model=StatusResponse)
async def status(request: Request):
    """
    Allows the frontend to verify that a user's Spotify access token is present / user is logged in with Spotify
    """
    # TODO: Ensure we use the refresh token if the token is expired
    # (this could be done by hitting some endpoint on spotify, checking for denied access, then hitting the refresh endpoint, instead of checking our session/token)

    session_cookie = request.cookies.get(settings.session_cookie)
    if not session_cookie:
        return StatusResponse(authenticated=False)

    try:
        session = decode_cookie(session_cookie, max_age=settings.session_cookie_max_age)
    except (SignatureExpired, BadSignature):
        return StatusResponse(authenticated=False)

    access_token = session.get("access_token")
    expires_at = session.get("expires_at", 0)
    if not access_token or int(time.time()) >= int(expires_at):
        return StatusResponse(authenticated=False)

    scopes = session.get("scope")
    return StatusResponse(authenticated=True, scopes=scopes.split())
