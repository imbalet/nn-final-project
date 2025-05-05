from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
import json
from pytubefix import YouTube

from services import SummarizeService
from schemas import Task
from schemas import Result
from video_processor.utils import get_metadata, download_video, transcribe_audio


def process_video(task: Task, summarizer: SummarizeService) -> Result:
    try:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(YouTube, task.url)
            youtube = future.result(timeout=5)
            future = executor.submit(lambda: youtube.streams)
            future.result(timeout=10)

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
    except Exception as e:
        print(e)
        return Result(
            id=task.id,
            title="",
            preview_link="",
            status="error",
            summary="",
        )
