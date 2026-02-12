from fastapi import APIRouter
from .user import router as user_router
from .top_items import router as top_items_router
from .playback import router as playback_router

router = APIRouter()

router.include_router(user_router, tags=['User'])
router.include_router(top_items_router, tags=['Top Items'])
router.include_router(playback_router, tags=['Playback'])
