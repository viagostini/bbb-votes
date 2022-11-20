from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from sqlalchemy.orm import Session, mapper

from bbb.core import Participant

metadata = MetaData()

participants = Table(
    "participants",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50), nullable=False),
    Column("votes", Integer, default=0),
)

participants_mapper = mapper(Participant, participants)

engine = create_engine("postgresql+psycopg2://admin:admin@db/admin", echo=True, future=True)
session = Session(engine)
