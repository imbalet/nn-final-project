from abc import ABC
from schemas import Task
from schemas import Result


class BaseRepo(ABC):
    async def get_task(self) -> Task | None: ...

    async def set_result(self, result: Result) -> None: ...
