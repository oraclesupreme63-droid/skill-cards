import asyncio

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import ReferenceCard

CORE_SKILL_NAMES = [
    "Comunicación",
    "Disciplina/constancia",
    "Resolución de problemas",
    "Regulación emocional",
]

REFERENCE_CARDS = [
    {
        "name": "Ryan Holiday",
        "photo_url": "/static/ryan-holiday.jpg",
        "description": (
            "Escritor y estratega de marketing estadounidense, referente del "
            "estoicismo aplicado a la vida moderna. Autor de libros como "
            "El Obstáculo es el Camino, El Ego es el Enemigo y The Daily Stoic. "
            "Fundador de la agencia Brass Check y dueño de The Painted Porch "
            "Bookshop, su librería física en Bastrop, Texas."
        ),
    },
    {
        "name": "Adrià Solà Pastor",
        "photo_url": "/static/adria-sola-pastor.jpg",
        "description": (
            "Emprendedor, divulgador y creador de contenido español "
            "especializado en comunicación, desarrollo personal y negocios "
            "digitales. Fundador del Instituto de Comunicación y de Fidelio, "
            "enseña a hablar con confianza, negociar y construir marca "
            "personal a una audiencia de millones de seguidores en YouTube "
            "y redes."
        ),
    },
]


async def seed_reference_cards() -> None:
    async with AsyncSessionLocal() as session:
        for card_data in REFERENCE_CARDS:
            existing = await session.scalar(
                select(ReferenceCard).where(ReferenceCard.name == card_data["name"])
            )
            if existing is None:
                session.add(ReferenceCard(**card_data))
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_reference_cards())
