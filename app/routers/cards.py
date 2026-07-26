from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.core.rarity import calculate_rarity
from app.database import get_db
from app.models import User, UserSkill
from app.schemas import SkillCardRead

router = APIRouter(tags=["cards"])


@router.get("/cards", response_model=list[SkillCardRead])
async def list_cards(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.scalars(
        select(UserSkill).where(UserSkill.user_id == current_user.id)
    )
    return [
        SkillCardRead(
            id=skill.id,
            name=skill.name,
            is_core=skill.is_core,
            level=skill.level,
            rarity=calculate_rarity(skill.level),
        )
        for skill in result.all()
    ]
