from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base

Base = declarative_base()


class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    votes = Column(Integer, default=0)


engine = create_engine("postgresql+psycopg2://admin:admin@db/admin", echo=True, future=True)
session = Session(engine)
