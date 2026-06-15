# Swim Project Backend
 
A REST API backend for a swimming activity & competition platform — users log swims, set goals, track equipment, join competitions and challenges, and compete on leaderboards.
 
This is a personal/portfolio project focused on practicing production-style backend architecture: clean app structure, secure authentication, meaningful business logic, containerization, and automated testing.
 
> Design reference: [Figma board](https://www.figma.com/board/xLMmTUszFSQzNmnz6KAKhr/graph-swim?node-id=0-1&p=f&t=Z7atVqBa6TGgzOUD-0)

**Stack:** Python · Flask · PostgreSQL · SQLAlchemy · Alembic · JWT · OAuth2 (Authlib) · Docker · Pytest
---
 
## Features
 
- **Authentication** — Facebook OAuth 2.0 login (Authlib) + JWT access/refresh tokens, with custom handlers for expired/invalid/missing tokens and a token-blacklist for secure logout
- **Activities** — log swimming activities (distance, speed, etc.)
- **Goals** — set personal goals; status is automatically updated based on activity progress
- **Equipment** — track equipment usage, with validation on type and breakage
- **Competitions** — join competitions, with a managed status lifecycle
- **Challenges** — linked to activities, with automatic winner calculation
- **Leaderboards / Ratings** — rankings per competition, per challenge, and a global leaderboard
- **Testing** — unit and integration tests (Pytest, factory_boy, Faker, coverage, custom `integration` marker)

 

## Getting Started
 
### Prerequisites
 
- Docker & Docker Compose
### Setup
 
1. Clone the repository:
```bash
   git clone https://github.com/Quzay/swim_proj.git
   cd swim_proj
```
 
2. Create a `.env` file in the project root with the following variables:
```env
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_DB=swim_db
   FLASK_DEBUG=1
   FLASK_SECRET_KEY=your_secret_key
   FLASK_JWT_SECRET_KEY=your_jwt_secret_key
   FLASK_JWT_ACCESS_TOKEN_EXPIRES=3600
   FLASK_JWT_REFRESH_TOKEN_EXPIRES=2592000
   FACEBOOK_CLIENT_ID=your_facebook_app_id
   FACEBOOK_CLIENT_SECRET=your_facebook_app_secret
```
 
3. Start the project:
```bash
   docker compose up --build
```
 
   For live-reload during development (syncs `app/` and `run.py` automatically, rebuilds on dependency changes):
```bash
   docker compose watch
```
 
The API will be available at `http://localhost:5000`. PostgreSQL runs with a health check, so the `web` service waits until the database is ready before starting.
 
---
 
##  Database Migrations
 
Database schema is managed with Alembic via Flask-Migrate:
 
```bash
flask db upgrade
```
 
---
 
##  Running Tests
 
```bash
pytest
```
 
Run only integration tests:
 
```bash
pytest -m integration
```
 
Test data is generated using `factory_boy` and `Faker` for realistic, repeatable test scenarios, with coverage tracked via `coverage`.
 

 
##  Status
 
Actively developed as a learning/portfolio project.