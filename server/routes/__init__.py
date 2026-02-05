from fastapi import APIRouter
from .auth import router as auth_router
from .spotify import router as spotify_router

main_router = APIRouter()

main_router.include_router(auth_router, tags=['Auth'])
main_router.include_router(spotify_router, tags=['Spotify'])
