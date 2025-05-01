from schemas.task import Task
from schemas.result import Result
from video_processor.utils import get_metadata, download_video, transcribe_audio
from pytubefix import YouTube


def process_video(task: Task) -> Result:
    try:
        youtube = YouTube(task.url)
        metadata = get_metadata(youtube)
        path = download_video(youtube)
        result = transcribe_audio(path)
        text = result["text"]

        return Result(
            id=task.id,
            title=metadata.title,
            preview_link=metadata.preview_link,
            status="done",
            summary=text,
        )
    except Exception:
        return Result(
            id=task.id,
            title="",
            preview_link="",
            status="error",
            summary="",
        )
