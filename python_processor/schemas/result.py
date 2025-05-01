from dataclasses import dataclass


@dataclass
class Result:
    id: str
    title: str
    preview_link: str
    status: str
    summary: str
