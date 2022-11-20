from dataclasses import dataclass

import faust


@dataclass
class Participant:
    id: int
    name: str
    votes: int = 0


class Vote(faust.Record):
    participant_id: int


def count_votes(votes: list[Vote]) -> dict[int, int]:
    votes_to_id = {1: 0, 2: 0, 3: 0}

    for vote in votes:
        votes_to_id[vote.participant_id] += 1

    return votes_to_id


def add_votes(participants: list[Participant], votes_to_id: dict[int, int]):
    for participant in participants:
        participant.votes += votes_to_id[participant.id]
