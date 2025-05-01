import traceback


class AppError(Exception):
    def __init__(
        self,
        message: str,
        cause: Exception = None,
    ):
        super().__init__(message)
        self.cause = cause
        self.traceback = traceback.format_exc()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {super().__str__()}"


class VideoUnavailableError(AppError):
    def __init__(self, message, cause=None):
        super().__init__(message, cause)


class VideoDownloadError(AppError):
    def __init__(self, message, cause=None):
        super().__init__(message, cause)
