import asyncio

from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Question, ReferenceCard

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

# Mismos tramos que la rareza: bronce, plata, oro, platino, dios.
LEVEL_BANDS = [(1, 20), (21, 40), (41, 60), (61, 80), (81, 100)]

QUESTION_PROMPTS = {
    "Comunicación": [
        "Contá una situación reciente donde tuviste que explicar algo a otra "
        "persona y lograste que te entendiera.",
        "Contá una situación donde tuviste que comunicar algo difícil o "
        "incómodo (una mala noticia, decir que no, corregir a alguien) y "
        "cómo lo manejaste.",
        "Contá una situación donde tuviste que persuadir a alguien que no "
        "estaba de acuerdo con vos, sin generar un conflicto.",
        "Contá una situación donde hablaste frente a un grupo y lograste "
        "que tu mensaje quedara claro y memorable.",
        "Contá una situación donde tu forma de comunicar cambió el "
        "resultado de algo importante: una negociación, una decisión "
        "grupal, un conflicto serio.",
    ],
    "Disciplina/constancia": [
        "Contá algo que vengas haciendo de forma constante en las últimas "
        "dos semanas, aunque no tuvieras ganas algún día.",
        "Contá un hábito que sostuviste durante al menos un mes, incluso "
        "en una semana mala.",
        "Contá una meta de varios meses en la que seguiste avanzando "
        "aunque no veías resultados inmediatos.",
        "Contá una situación donde elegiste algo que te convenía a largo "
        "plazo en vez de lo cómodo/fácil ahora.",
        "Contá un hábito o proyecto que sostuviste por más de un año, y "
        "qué sistema armaste para que no dependiera de tu ánimo del día.",
    ],
    "Resolución de problemas": [
        "Contá un problema cotidiano que resolviste sin ayuda de nadie.",
        "Contá un problema donde tu primera solución no funcionó y "
        "tuviste que probar otra cosa.",
        "Contá un problema complejo que resolviste dividiéndolo en partes "
        "más chicas.",
        "Contá una situación donde resolviste un problema que afectaba a "
        "otras personas, no solo a vos.",
        "Contá un problema grande que, mirándolo en retrospectiva, cambió "
        "cómo enfrentás problemas parecidos desde entonces.",
    ],
    "Regulación emocional": [
        "Contá una situación reciente donde te enojaste o frustraste, "
        "pero no reaccionaste mal en el momento.",
        "Contá un conflicto donde, aunque tenías razón para enojarte, "
        "elegiste bajar la intensidad en vez de escalarlo.",
        "Contá una situación de mucha presión donde mantuviste la calma "
        "lo suficiente como para pensar con claridad.",
        "Contá una situación donde alguien te provocó directamente y "
        "respondiste de forma medida en vez de a la defensiva.",
        "Contá una crisis o conflicto serio donde tu manejo emocional "
        "evitó que la situación empeorara para vos o para otros.",
    ],
    None: [
        "Contá una situación reciente donde aplicaste esta habilidad de "
        "forma básica, y funcionó.",
        "Contá una situación donde tuviste que aplicarla bajo cierta "
        "dificultad (poco tiempo, poca práctica previa, algo salió "
        "distinto a lo esperado).",
        "Contá una situación donde esta habilidad te permitió resolver "
        "algo que sin ella no hubieras podido.",
        "Contá una situación donde alguien notó o se benefició "
        "directamente de tu nivel en esta habilidad.",
        "Contá una situación donde esta habilidad ya es parte de cómo te "
        "identificás: algo que harías casi sin pensar.",
    ],
}


def _build_questions() -> list[dict]:
    questions = []
    for skill_name, prompts in QUESTION_PROMPTS.items():
        for (min_level, max_level), prompt in zip(LEVEL_BANDS, prompts):
            questions.append(
                {
                    "skill_name": skill_name,
                    "min_level": min_level,
                    "max_level": max_level,
                    "prompt": prompt,
                }
            )
    return questions


QUESTIONS = _build_questions()


async def seed_reference_cards() -> None:
    async with AsyncSessionLocal() as session:
        for card_data in REFERENCE_CARDS:
            existing = await session.scalar(
                select(ReferenceCard).where(ReferenceCard.name == card_data["name"])
            )
            if existing is None:
                session.add(ReferenceCard(**card_data))
        await session.commit()


async def seed_questions() -> None:
    async with AsyncSessionLocal() as session:
        for q in QUESTIONS:
            existing = await session.scalar(
                select(Question).where(
                    Question.skill_name == q["skill_name"],
                    Question.min_level == q["min_level"],
                    Question.max_level == q["max_level"],
                )
            )
            if existing is None:
                session.add(Question(**q))
        await session.commit()


async def seed_all() -> None:
    await seed_reference_cards()
    await seed_questions()


if __name__ == "__main__":
    asyncio.run(seed_all())
