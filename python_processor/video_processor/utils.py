from pathlib import Path
from pytubefix import YouTube, Stream
from pytubefix.exceptions import VideoUnavailable, RegexMatchError
import re
import shutil
import whisper
from tempfile import mkdtemp

from exceptions import (
    VideoDownloadError,
    VideoUnavailableError,
)
from schemas import Metadata


def get_metadata(yt: YouTube) -> Metadata:
    preview = yt.thumbnail_url
    title = yt.title
    return Metadata(title=title, preview_link=preview)


def download_video(yt: YouTube) -> Path:
    try:
        stream: Stream = yt.streams.filter(type="audio").order_by("abr").last()

        if not stream:
            raise VideoDownloadError("No audio stream available")
        temp_dir = Path(mkdtemp(prefix="youtube_dl_"))
        path: str = stream.download(
            temp_dir,
            filename=re.sub(r"[^\w\-_\.]", "_", stream.title),
            timeout=10,
        )
        path = Path(path)
        if not path:
            raise VideoDownloadError("Video download failed")
    except RegexMatchError as e:
        raise VideoUnavailableError("Regexp error", e) from e
    except VideoUnavailable as e:
        raise VideoUnavailableError("Video unavailable", e) from e
    except VideoDownloadError as e:
        raise e
    except Exception as e:
        raise VideoDownloadError("Unexpected video download error", e) from e
    return path


def transcribe_audio(path: Path, model_name="base") -> dict:
    try:
        model = whisper.load_model(model_name)
        result = model.transcribe(str(path))
        return result
    finally:
        shutil.rmtree(path.parent, ignore_errors=True)
