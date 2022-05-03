import faust
from pydantic import BaseSettings


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
    print([vote.asdict() for vote in votes])


@app.agent(votes_topic)
async def process(votes: faust.Stream):
    async for batch in votes.take(config.batch_size, within=config.batch_window_seconds):
        process_votes(batch)
