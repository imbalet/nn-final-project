from pydantic import BaseModel


class VideoRequest(BaseModel):
    url: str


class VideoResponse(BaseModel):
    transcription: str
