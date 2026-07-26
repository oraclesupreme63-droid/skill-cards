from app.models import ReferenceCard, ReferenceCardSkill
from tests.conftest import TestSessionLocal


async def _seed_reference_card() -> None:
    async with TestSessionLocal() as session:
        card = ReferenceCard(
            name="Ryan Holiday",
            photo_url="/static/ryan-holiday.jpg",
            description="Escritor sobre estoicismo moderno.",
            overall_rarity="Legendary",
            role="Wisdom Support",
        )
        card.skills = [
            ReferenceCardSkill(name="Comunicación", is_core=True, level=98),
            ReferenceCardSkill(name="Estoicismo", is_core=False, level=100),
        ]
        session.add(card)
        await session.commit()


async def test_list_reference_cards_does_not_require_auth(client):
    await _seed_reference_card()
    response = await client.get("/reference-cards")
    assert response.status_code == 200
    cards = response.json()
    assert len(cards) == 1

    card = cards[0]
    assert card["name"] == "Ryan Holiday"
    assert card["overall_rarity"] == "Legendary"
    assert len(card["skills"]) == 2

    estoicismo = next(s for s in card["skills"] if s["name"] == "Estoicismo")
    assert estoicismo["level"] == 100
    assert estoicismo["rarity"] == "dios"
