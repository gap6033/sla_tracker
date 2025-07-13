# SLA Tracker

This project is an SLA tracking service built with FastAPI, PostgreSQL, and Redis. It uses Docker and Docker Compose to set up and run the entire stack easily.

---

## Features

- SLA clock tracking in PostgreSQL
- Alert queueing with Redis
- Background SLA breach checks and notifications
- Fully containerized for easy setup and deployment

---

## Prerequisites

- Docker (version 20.x or later recommended)
- Docker Compose (version 1.29+ or Docker Compose v2)

---

## Getting Started

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/sla-tracker.git
   cd sla-tracker


## Create a .env file in the root directory with the following content (adjust values as needed):

POSTGRES_DB=slatrackerdb
POSTGRES_USER=gaurang
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
POSTGRES_HOST=postgres

## Build and start containers

docker-compose up --build

This will start 3 services:
 - FastAPI app on port 8000

 - PostgreSQL database

 - Redis server

## Check this endpoint

http://127.0.0.1:8000/api/v1/ -> If you get {"status":"running"}. The service is running

## To check FastAPI service logs run below command in terminal
docker logs -f sla_fastapi


## To Access PostGres Container Shell run below command in terminal
docker exec -it sla_postgres psql -U ${POSTGRES_USER} -d slatrackerdb

## To Access Redis Container Shell run below command in terminal
docker exec -it sla_redis redis-cli


## Notes
Make sure ports used for FastAPI service, PostGres and Redis CLI are free on your host machine or adjust .env and docker-compose.yml accordingly.

This setup assumes Docker and Docker Compose are installed and running on your machine.
