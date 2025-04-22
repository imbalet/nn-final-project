from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes.video_transcriber import router as video_router

app = FastAPI()
app.include_router(video_router, tags=["video_transcriber"])

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
