from dataclasses import asdict
import json
from pytubefix import YouTube

from services import SummarizeService
from schemas import Task
from schemas import Result
from video_processor.utils import get_metadata, download_video, transcribe_audio


def process_video(task: Task, summarizer: SummarizeService) -> Result:
    try:
        youtube = YouTube(task.url)
        metadata = get_metadata(youtube)
        path = download_video(youtube)
        result = transcribe_audio(path)
        stamps = summarizer.summarize_video(result)
        text = json.dumps([asdict(i) for i in stamps], ensure_ascii=False)

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
