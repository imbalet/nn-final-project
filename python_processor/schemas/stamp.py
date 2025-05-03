from dataclasses import dataclass


@dataclass
class Stamp:
    start: float
    end: float
    text: str


@dataclass
class ExtendedStamp(Stamp):
    start_sym: int
    end_sym: int
