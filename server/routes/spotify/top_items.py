import httpx
from fastapi import APIRouter, Request, HTTPException
from schema import ServerSettings, ContentSettings, ProfileImage, UserProfile , UserTopItems
from dotenv import load_dotenv
from utils import InvalidSessionError, AuthenticationError, get_token
from typing import List, Optional,Literal
from pydantic import ValidationError

load_dotenv()
settings = ServerSettings()
router = APIRouter(prefix="/spotify")

@router.get("/top-items",response_model=UserTopItems)
async def get_top_items(request: Request,
                        type: Literal["artists", "tracks"],):
    """
    Gets the user's top tracks from Spotify.
    """
    session_cookie = request.cookies.get(settings.session_cookie)
    if not session_cookie:
        raise HTTPException(status_code=404, detail="No session found")
    
    try:
        access_token = get_token(session_cookie)
    except (InvalidSessionError, AuthenticationError):
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    headers = {"Authorization": f"Bearer {access_token}"}
    async with httpx.AsyncClient(timeout=20) as client:
        res = await client.get(f"{settings.spotify_base_url}/me/top/{type}", headers=headers)
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to fetch top items from Spotify: {res.text}")
        
        response = res.json()

    return {
        "type": type,
        **response}