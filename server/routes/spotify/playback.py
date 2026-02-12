import httpx
from fastapi import APIRouter, Request, HTTPException
from schema import ServerSettings, RecentlyPlayed
from dotenv import load_dotenv
from utils import InvalidSessionError, AuthenticationError, get_token
from typing import List, Optional,Literal
from pydantic import ValidationError

load_dotenv()
settings=ServerSettings()
router = APIRouter(prefix="/spotify")

@router.get("/recently-played",response_model=RecentlyPlayed) 
async def get_recently_played(request: Request):
    """
    Gets the user's recently played tracks from Spotify.
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
        res = await client.get(f"{settings.spotify_base_url}/me/player/recently-played", headers=headers)
        if res.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to fetch recently played tracks from Spotify: {res.text}")
        
        response = res.json()

    return response 
