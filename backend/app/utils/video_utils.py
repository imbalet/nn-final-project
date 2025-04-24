import whisper
from pytubefix import YouTube, Stream
from pytubefix.exceptions import VideoUnavailable, RegexMatchError
from backend.app.exceptions.video_exceptions import (
    VideoDownloadError,
    VideoUnavailableError,
)
from tempfile import mkdtemp
from pathlib import Path
import shutil
import re


def download_video(url: str) -> Path:
    try:
        yt = YouTube(url)
        stream: Stream = yt.streams.filter(type="audio").order_by("abr").last()

        if not stream:
            raise VideoDownloadError("No audio stream available")
        temp_dir = Path(mkdtemp(prefix="youtube_dl_"))
        path = stream.download(
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


def transcribe_audio(path: Path, model_name="base") -> str:
    model = whisper.load_model(model_name)
    result = model.transcribe(str(path))
    shutil.rmtree(path.parent, ignore_errors=True)
    return result["text"]
