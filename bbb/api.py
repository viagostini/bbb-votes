import json

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI

api = FastAPI()

KAFKA_HOST_URL = "localhost:9092"
KAFKA_VOTES_TOPIC = "votes"

producer = AIOKafkaProducer(
    bootstrap_servers=KAFKA_HOST_URL,
    value_serializer=lambda x: json.dumps(x).encode(),
)


@api.on_event("startup")
async def start_producer():
    await producer.start()


@api.on_event("shutdown")
async def stop_producer():
    await producer.stop()


@api.get("/vote/{participant_id}")
async def vote(participant_id: int):
    await producer.send_and_wait(KAFKA_VOTES_TOPIC, {"participant_id": participant_id})

    return {"status": "OK", "participant_id": participant_id}
