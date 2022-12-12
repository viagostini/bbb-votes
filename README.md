## Big Brother Brasil Voting

This is my take on implementing the backend for Big Brother Brasil's voting system. In order to serve a high voting throughput, the votes are processed asynchronously using a message broker.

## Frameworks and tech
* API: Python + FastAPI
* DB: PostgreSQL
* Message broker: Redpanda (Kafka-compatible API)
* Message processing: Faust

## How to run it
You will need access to make, docker and docker-compose.

```
make build
make start
``` 

This will start everything. You can vote by sending a request to `http://localhost:8000/vote/{:id}`.

To check the current vote count, you can use `make check-votes`. Note that because the vote processing is async you may not see the latest votes in the table instantly.