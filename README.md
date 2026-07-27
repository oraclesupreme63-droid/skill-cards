# Skill Cards

Backend for a FIFA-style card system that measures real-life skills (mostly social ones). Each skill has a level you raise yourself, validated through an honest self-assessment system, and a rarity calculated automatically from that level — it's never stored in the database.

A personal backend portfolio/learning project, no frontend: [Swagger](#usage) (`/docs`) is the testing interface.

## Stack

- Python 3.12 + FastAPI
- PostgreSQL + SQLAlchemy 2.0 (async)
- Alembic (migrations)
- JWT (python-jose) + bcrypt (passlib)
- Pydantic v2
- Docker + docker-compose
- Pytest + httpx + pytest-asyncio (in-memory SQLite for tests)

## Getting started

Requirements: Docker Desktop installed and running.

```bash
git clone https://github.com/oraclesupreme63-droid/skill-cards.git
cd skill-cards
docker compose up -d --build
```

First run: apply migrations and seed the initial data (4 core skills, 25 questions for the level-up validation system, 2 reference cards).

```bash
docker compose exec api alembic upgrade head
docker compose exec api python -m app.seed.seed_data
```

The API is available at `http://localhost:8000`, interactive docs at `http://localhost:8000/docs`.

## Usage

1. `POST /auth/register` — create a user (email + password). You automatically get 4 core skills at level 1.
2. In `/docs`, click **Authorize** (the padlock at the top of the page) with the same email/password — this authenticates every following request. (Note: testing `/auth/login` with "Try it out" does *not* do the same thing, it only returns the token in the response.)
3. `GET /skills` — list your skills.
4. `POST /skills` — create a custom skill (maximum 2 per user).
5. `GET /skills/{id}/question` — fetch the question/scenario needed to level up that skill.
6. `PATCH /skills/{id}/level` — answer the question and confirm whether you passed it (`self_confirmed`). If `true`, the level goes up.
7. `GET /skills/{id}/history` — view that skill's level-up history.
8. `GET /cards` — your skills with rarity already calculated, ready to be rendered as cards.
9. `GET /reference-cards` — reference cards (Ryan Holiday, Adrià Solà Pastor), read-only and public (no authentication required).

## Business rules

- On registration, 4 core skills are created automatically: Comunicación, Disciplina/constancia, Resolución de problemas, Regulación emocional.
- Maximum 2 custom skills per user — the third one returns `400`.
- Rarity is always calculated from the level, never persisted: 1-20 bronce, 21-40 plata, 41-60 oro, 61-80 platino, 81-100 dios.
- Leveling up requires answering a question/scenario and self-confirming whether you passed it — it's not a plain counter you bump yourself. Every attempt (passed or not) is recorded.

## Tests

```bash
docker compose exec api pytest -v
```

Tests run against an in-memory SQLite database, independent from the real one — you don't need Postgres running to execute them (you do need the `api` container running, since that's where the dependencies are installed).

## Project structure

```text
app/
├── main.py              # FastAPI app, routers, /health, /static
├── database.py           # async engine, sessionmaker, Base
├── models.py             # SQLAlchemy models
├── schemas.py             # Pydantic schemas
├── core/
│   ├── config.py         # settings (environment variables)
│   ├── security.py        # hashing, JWT
│   └── rarity.py          # rarity calculation
├── auth/
│   ├── router.py          # /auth/register, /auth/login
│   └── dependencies.py    # get_current_user
├── routers/
│   ├── skills.py           # /skills
│   ├── cards.py             # /cards
│   └── reference_cards.py   # /reference-cards
├── seed/
│   └── seed_data.py         # core skills, questions, reference cards
└── static/                  # reference card photos

alembic/                  # migrations
tests/                    # pytest test suite
```
