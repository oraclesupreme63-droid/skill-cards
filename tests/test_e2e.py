from app.models import Question, ReferenceCard, ReferenceCardSkill
from tests.conftest import TestSessionLocal


async def test_full_flow_register_to_cards(client):
    # 1. Registro: crea el usuario y sus 4 skills core
    register = await client.post(
        "/auth/register", json={"email": "e2e@test.com", "password": "12345678"}
    )
    assert register.status_code == 201

    # 2. Login: autenticación
    login = await client.post(
        "/auth/login", data={"username": "e2e@test.com", "password": "12345678"}
    )
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Las 4 skills core ya existen en nivel 1
    skills = (await client.get("/skills", headers=headers)).json()
    assert len(skills) == 4
    assert all(s["level"] == 1 for s in skills)

    # 4. Crear 2 skills custom, la 3ra falla
    assert (
        await client.post("/skills", json={"name": "Programación"}, headers=headers)
    ).status_code == 201
    assert (
        await client.post("/skills", json={"name": "Idiomas"}, headers=headers)
    ).status_code == 201
    assert (
        await client.post("/skills", json={"name": "Guitarra"}, headers=headers)
    ).status_code == 400

    skills = (await client.get("/skills", headers=headers)).json()
    assert len(skills) == 6

    # 5. Subir de nivel una skill core: pedir la pregunta, responder, confirmar
    async with TestSessionLocal() as session:
        session.add(
            Question(
                skill_name=None,
                min_level=1,
                max_level=100,
                prompt="Contá una situación donde aplicaste esta habilidad.",
            )
        )
        await session.commit()

    core_skill = next(s for s in skills if s["is_core"])
    question = (
        await client.get(f"/skills/{core_skill['id']}/question", headers=headers)
    ).json()

    level_up = await client.patch(
        f"/skills/{core_skill['id']}/level",
        json={
            "question_id": question["id"],
            "answer_text": "Situación real y concreta.",
            "self_confirmed": True,
        },
        headers=headers,
    )
    assert level_up.status_code == 200
    assert level_up.json()["level"] == 2

    history = (
        await client.get(f"/skills/{core_skill['id']}/history", headers=headers)
    ).json()
    assert len(history) == 1
    assert history[0]["level"] == 2

    # 6. /cards: la rareza se calcula, todas siguen en bronce (niveles 1-2)
    cards = (await client.get("/cards", headers=headers)).json()
    assert len(cards) == 6
    assert all(c["rarity"] == "bronce" for c in cards)

    # 7. /reference-cards: público, sin autenticación
    async with TestSessionLocal() as session:
        card = ReferenceCard(
            name="Ryan Holiday",
            photo_url="/static/ryan-holiday.jpg",
            description="Escritor sobre estoicismo moderno.",
            overall_rarity="Legendary",
            role="Wisdom Support",
        )
        card.skills = [ReferenceCardSkill(name="Estoicismo", is_core=False, level=100)]
        session.add(card)
        await session.commit()

    reference_cards = (await client.get("/reference-cards")).json()
    assert len(reference_cards) == 1
    assert reference_cards[0]["skills"][0]["rarity"] == "dios"

    # 8. Sin token, /skills sigue protegido
    assert (await client.get("/skills")).status_code == 401
