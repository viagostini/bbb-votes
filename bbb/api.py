import json

from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from pydantic import BaseSettings, conint


class Config(BaseSettings):
    kafka_host_url: str
    kafka_votes_topic: str


config = Config()

producer = AIOKafkaProducer(
    bootstrap_servers=config.kafka_host_url,
    value_serializer=lambda x: json.dumps(x).encode(),
)

api = FastAPI()


@api.on_event("startup")
async def start_producer():
    await producer.start()


@api.on_event("shutdown")
async def stop_producer():
    await producer.stop()


@api.get("/vote/{participant_id}", status_code=202)
async def vote(participant_id: conint(ge=1, le=3)):
    await producer.send(config.kafka_votes_topic, {"participant_id": participant_id})

    return {"status": "OK", "participant_id": participant_id}
