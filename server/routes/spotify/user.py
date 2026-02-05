import httpx
from fastapi import APIRouter, Request, HTTPException
from schema import ServerSettings, ContentSettings, ProfileImage, UserProfile
from dotenv import load_dotenv
from utils import InvalidSessionError, AuthenticationError, get_token


load_dotenv()
settings = ServerSettings()
router = APIRouter(prefix="/spotify")


@router.get("/profile")
async def get_profile(request: Request) -> UserProfile:
    """
    Gets the users session cookie, validates it, and then requests the user's profile information from Spotify.

    Spotify docs:
    - https://developer.spotify.com/documentation/web-api/reference/get-current-users-profile
    """

    session_cookie = request.cookies.get(settings.session_cookie)
    if not session_cookie:
        raise HTTPException(status_code=404, detail="No session found")
    
    try:
        access_token = get_token(session_cookie)
    except (InvalidSessionError, AuthenticationError):
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    response = {}
    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient(timeout=20) as client:
        res = await client.get(f"{settings.spotify_base_url}/me", headers=headers)
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to fetch user profile from Spotify: {res.text}")

        response = res.json()

    if not response:
        raise HTTPException(status_code=400, detail="No payload received from Spotify")
    
    return UserProfile(
        country_code=response["country"],
        name=response["display_name"],
        email=response["email"],
        content_settings=ContentSettings(
            enabled=response["explicit_content"]["filter_enabled"],
            locked=response["explicit_content"]["filter_locked"]
        ),
        player_url=response["external_urls"]["spotify"],
        follower_count=response["followers"]["total"],
        web_api=response["href"],
        spotify_id=response["id"],
        profile_images=[ProfileImage(
            url=image["url"],
            height=image["height"],
            width=image["width"]
        ) for image in response.get("images", [])],
        premium = {"free": False, "premium": True}.get(response["product"]),
        user_uri=response["uri"]
    )

