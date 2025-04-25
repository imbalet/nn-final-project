from pydantic import BaseModel


class VideoRequest(BaseModel):
    url: str


class VideoResponse(BaseModel):
    transcription: str
    video_preview: bytes
    video_title: str
    url: str
