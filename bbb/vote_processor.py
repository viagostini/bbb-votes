import faust
from pydantic import BaseSettings
from sqlalchemy import select

from bbb.db import Participant, session


class Config(BaseSettings):
    kafka_host_url: str
    batch_size: int
    batch_window_seconds: int


class Vote(faust.Record):
    participant_id: int


config = Config()

app = faust.App("vote_processor", broker=config.kafka_host_url)
votes_topic = app.topic("votes", value_type=Vote)


def process_votes(votes: list[Vote]):
    votes_to_id = {1: 0, 2: 0, 3: 0}

    for vote in votes:
        votes_to_id[vote.participant_id] += 1

    for participant in session.scalars(select(Participant)):
        participant.votes += votes_to_id[participant.id]

    session.commit()


@app.agent(votes_topic)
async def process(votes: faust.Stream):
    async for batch in votes.take(config.batch_size, within=config.batch_window_seconds):
        process_votes(batch)
