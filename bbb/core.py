from dataclasses import dataclass


@dataclass
class Participant:
    id: int
    name: str
    votes: int = 0

