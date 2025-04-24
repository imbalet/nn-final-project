import asyncio
import shutil
from concurrent.futures import ProcessPoolExecutor
from fastapi.routing import APIRouter
from fastapi import HTTPException
from backend.app.schemas.video_request import VideoRequest, VideoResponse
from backend.app.utils.video_utils import download_video, transcribe_audio


router = APIRouter(tags=["video_transcriber"])
executor = ProcessPoolExecutor(max_workers=4)


@router.post("/process_video")
async def process_video(request: VideoRequest) -> VideoResponse:
    try:
        url = request.url
        if not url:
            raise HTTPException(status_code=400, detail="URL не может быть пустым")

        if "youtube.com" not in url and "youtu.be" not in url:
            raise HTTPException(status_code=400, detail="Некорректный URL YouTube")

        path = await asyncio.to_thread(download_video, url)

        transcription = await asyncio.get_running_loop().run_in_executor(
            executor, transcribe_audio, path
        )

        return VideoResponse(transcription=transcription)

    except HTTPException as he:
        shutil.rmtree(path.parent, ignore_errors=True)
        raise he
    except Exception as e:
        shutil.rmtree(path.parent, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"Ошибка обработки видео: {str(e)}")
