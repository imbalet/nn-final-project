from abc import ABC
from schemas.task import Task
from schemas.result import Result


class BaseRepo(ABC):
    async def get_task(self) -> Task | None: ...

    async def set_result(self, result: Result) -> None: ...
