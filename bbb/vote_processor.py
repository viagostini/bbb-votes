import faust
from pydantic import BaseSettings
from sqlalchemy import select

from bbb.core import Participant, Vote, add_votes, count_votes
from bbb.db import session


class Config(BaseSettings):
    kafka_host_url: str
    batch_size: int
    batch_window_seconds: int


config = Config()

app = faust.App("vote_processor", broker=config.kafka_host_url)
votes_topic = app.topic("votes", value_type=Vote)


def process_votes(votes: list[Vote]):
    votes_to_id = count_votes(votes)
    participants = session.scalars(select(Participant))

    add_votes(participants, votes_to_id)

    session.commit()


@app.agent(votes_topic)
async def process(votes: faust.Stream):
    async for batch in votes.take(config.batch_size, within=config.batch_window_seconds):
        process_votes(batch)
