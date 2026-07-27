# Skill Cards

Backend de un sistema de cartas estilo FIFA para medir habilidades reales (sobre todo sociales). Cada habilidad ("skill") tiene un nivel que subís vos mismo, validado con un sistema de auto-evaluación honesta, y una rareza calculada automáticamente a partir de ese nivel — nunca se guarda en la base.

Proyecto de portafolio/aprendizaje backend, sin frontend: [Swagger](#uso) (`/docs`) es la interfaz de prueba.

## Stack

- Python 3.12 + FastAPI
- PostgreSQL + SQLAlchemy 2.0 (async)
- Alembic (migraciones)
- JWT (python-jose) + bcrypt (passlib)
- Pydantic v2
- Docker + docker-compose
- Pytest + httpx + pytest-asyncio (SQLite en memoria para tests)

## Cómo levantarlo

Requisitos: Docker Desktop instalado y corriendo.

```bash
git clone https://github.com/oraclesupreme63-droid/skill-cards.git
cd skill-cards
docker compose up -d --build
```

Primera vez: correr las migraciones y el seeding inicial (4 skills core, 25 preguntas del sistema de validación, 2 reference cards).

```bash
docker compose exec api alembic upgrade head
docker compose exec api python -m app.seed.seed_data
```

La API queda en `http://localhost:8000`, la documentación interactiva en `http://localhost:8000/docs`.

## Uso

1. `POST /auth/register` — creá un usuario (email + password). Se te crean automáticamente 4 skills core en nivel 1.
2. En `/docs`, click en **Authorize** (candado arriba de la página) con el mismo email/password — esto autentica todas las peticiones siguientes. (Ojo: probar `/auth/login` con "Try it out" *no* hace lo mismo, solo te devuelve el token en la respuesta.)
3. `GET /skills` — ver tus skills.
4. `POST /skills` — crear una skill personalizada (máximo 2 por usuario).
5. `GET /skills/{id}/question` — traer la pregunta/situación para subir al siguiente nivel de esa skill.
6. `PATCH /skills/{id}/level` — respondé la pregunta y confirmá si la aprobaste (`self_confirmed`). Si es `true`, el nivel sube.
7. `GET /skills/{id}/history` — ver el historial de subidas de esa skill.
8. `GET /cards` — tus skills con la rareza ya calculada, listas para pintar como cartas.
9. `GET /reference-cards` — cartas de referencia (Ryan Holiday, Adrià Solà Pastor), de solo lectura y sin necesidad de estar autenticado.

## Reglas de negocio

- Al registrarse, se crean automáticamente 4 skills core: Comunicación, Disciplina/constancia, Resolución de problemas, Regulación emocional.
- Máximo 2 skills personalizadas (custom) por usuario — la tercera devuelve `400`.
- La rareza se calcula siempre a partir del nivel, nunca se persiste: 1-20 bronce, 21-40 plata, 41-60 oro, 61-80 platino, 81-100 dios.
- Subir de nivel requiere responder una pregunta/situación y auto-confirmar si la aprobaste — no es un simple contador que subís vos sin más. Cada intento (apruebe o no) queda registrado.

## Tests

```bash
docker compose exec api pytest -v
```

Corren contra una base SQLite en memoria, independiente de la base real — no hace falta tener Postgres arriba para ejecutarlos (sí hace falta que el contenedor `api` esté corriendo, porque ahí están instaladas las dependencias).

## Estructura del proyecto

```text
app/
├── main.py              # FastAPI app, routers, /health, /static
├── database.py          # engine async, sessionmaker, Base
├── models.py            # modelos SQLAlchemy
├── schemas.py           # schemas Pydantic
├── core/
│   ├── config.py        # settings (variables de entorno)
│   ├── security.py      # hashing, JWT
│   └── rarity.py        # cálculo de rareza
├── auth/
│   ├── router.py         # /auth/register, /auth/login
│   └── dependencies.py   # get_current_user
├── routers/
│   ├── skills.py          # /skills
│   ├── cards.py           # /cards
│   └── reference_cards.py # /reference-cards
├── seed/
│   └── seed_data.py       # skills core, preguntas, reference cards
└── static/                # fotos de las reference cards

alembic/                  # migraciones
tests/                    # tests con pytest
```
