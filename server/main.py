import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import main_router
from schema import ServerSettings, RootResponse
from dotenv import load_dotenv

load_dotenv()

server = FastAPI(root_path="/api")
server.include_router(main_router)

settings = ServerSettings()

origins = os.getenv("CORS_ORIGINS", "").split(",")
origins = [origin for origin in origins if origin]

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@server.get("/", response_model=RootResponse, summary="Root endpoint", tags=["General"])
async def root():
    return RootResponse(
        message="Server hello"
    )

if __name__ == "__main__":
    uvicorn.run("main:server", host=settings.backend_host, port=settings.backend_port, reload=settings.debug)
