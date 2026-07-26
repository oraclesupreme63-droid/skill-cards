from app.models import Question
from tests.conftest import TestSessionLocal


async def _auth_headers(client, email: str, password: str = "12345678") -> dict:
    await client.post("/auth/register", json={"email": email, "password": password})
    login = await client.post(
        "/auth/login", data={"username": email, "password": password}
    )
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def _seed_generic_question() -> None:
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


async def test_register_creates_four_core_skills(client):
    headers = await _auth_headers(client, "skills1@test.com")
    response = await client.get("/skills", headers=headers)
    assert response.status_code == 200
    skills = response.json()
    assert len(skills) == 4
    assert all(s["is_core"] for s in skills)
    assert all(s["level"] == 1 for s in skills)


async def test_create_custom_skill(client):
    headers = await _auth_headers(client, "skills2@test.com")
    response = await client.post("/skills", json={"name": "Programación"}, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["is_core"] is False
    assert data["level"] == 1


async def test_third_custom_skill_fails(client):
    headers = await _auth_headers(client, "skills3@test.com")
    await client.post("/skills", json={"name": "Uno"}, headers=headers)
    await client.post("/skills", json={"name": "Dos"}, headers=headers)
    response = await client.post("/skills", json={"name": "Tres"}, headers=headers)
    assert response.status_code == 400


async def test_skills_require_authentication(client):
    response = await client.get("/skills")
    assert response.status_code == 401


async def test_level_up_with_self_confirmed_true(client):
    await _seed_generic_question()
    headers = await _auth_headers(client, "skills4@test.com")

    skills = (await client.get("/skills", headers=headers)).json()
    skill_id = skills[0]["id"]

    question = (
        await client.get(f"/skills/{skill_id}/question", headers=headers)
    ).json()

    response = await client.patch(
        f"/skills/{skill_id}/level",
        json={
            "question_id": question["id"],
            "answer_text": "Contexto real de la situación.",
            "self_confirmed": True,
        },
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["level"] == 2

    history = (
        await client.get(f"/skills/{skill_id}/history", headers=headers)
    ).json()
    assert len(history) == 1
    assert history[0]["level"] == 2


async def test_level_up_with_self_confirmed_false_does_not_change_level(client):
    await _seed_generic_question()
    headers = await _auth_headers(client, "skills5@test.com")

    skills = (await client.get("/skills", headers=headers)).json()
    skill_id = skills[0]["id"]

    question = (
        await client.get(f"/skills/{skill_id}/question", headers=headers)
    ).json()

    response = await client.patch(
        f"/skills/{skill_id}/level",
        json={
            "question_id": question["id"],
            "answer_text": "Todavía no me pasó algo así.",
            "self_confirmed": False,
        },
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json()["level"] == 1
