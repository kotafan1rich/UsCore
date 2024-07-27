from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.api.wish_list_handler import wish_list_router
from src.api.media_handler import media_router

app = FastAPI(title='UsCore')

main_api_router = APIRouter()

main_api_router.include_router(wish_list_router, prefix="/wishlist", tags=["Wishlist"])
main_api_router.include_router(media_router, prefix="/media", tags=["Media"])

app.include_router(main_api_router)
