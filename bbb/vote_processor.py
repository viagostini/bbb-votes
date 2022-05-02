import faust

KAFKA_HOST_URL = "localhost:9092"
BATCH_SIZE = 5
BATCH_WINDOW_SECONDS = 10


class Vote(faust.Record):
    participant_id: int


app = faust.App("vote_processor", broker=KAFKA_HOST_URL)
votes_topic = app.topic("votes", value_type=Vote)


def process_votes(votes: list[Vote]):
    print([vote.asdict() for vote in votes])


@app.agent(votes_topic)
async def process(votes: faust.Stream):
    async for batch in votes.take(BATCH_SIZE, within=BATCH_WINDOW_SECONDS):
        process_votes(batch)
