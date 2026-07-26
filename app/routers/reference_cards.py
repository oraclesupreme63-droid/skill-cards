from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.rarity import calculate_rarity
from app.database import get_db
from app.models import ReferenceCard
from app.schemas import ReferenceCardRead, ReferenceCardSkillRead

router = APIRouter(prefix="/reference-cards", tags=["reference-cards"])


@router.get("", response_model=list[ReferenceCardRead])
async def list_reference_cards(db: AsyncSession = Depends(get_db)):
    result = await db.scalars(
        select(ReferenceCard).options(selectinload(ReferenceCard.skills))
    )
    return [
        ReferenceCardRead(
            id=card.id,
            name=card.name,
            photo_url=card.photo_url,
            description=card.description,
            overall_rarity=card.overall_rarity,
            role=card.role,
            skills=[
                ReferenceCardSkillRead(
                    name=skill.name,
                    is_core=skill.is_core,
                    level=skill.level,
                    rarity=calculate_rarity(skill.level),
                )
                for skill in card.skills
            ],
        )
        for card in result.all()
    ]
