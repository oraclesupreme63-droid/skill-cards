from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models import LevelUpAttempt, Question, SkillLevelLog, User, UserSkill
from app.schemas import (
    LevelUpRequest,
    QuestionRead,
    SkillCreate,
    SkillLevelLogRead,
    SkillRead,
)

router = APIRouter(prefix="/skills", tags=["skills"])


@router.get("", response_model=list[SkillRead])
async def list_skills(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.scalars(
        select(UserSkill).where(UserSkill.user_id == current_user.id)
    )
    return result.all()


@router.get("/{skill_id}/question", response_model=QuestionRead)
async def get_question_for_skill(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    skill = await db.get(UserSkill, skill_id)
    if skill is None or skill.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill no encontrada")

    target_level = skill.level + 1

    question = await db.scalar(
        select(Question).where(
            Question.skill_name == skill.name,
            Question.min_level <= target_level,
            Question.max_level >= target_level,
        )
    )
    if question is None:
        question = await db.scalar(
            select(Question).where(
                Question.skill_name.is_(None),
                Question.min_level <= target_level,
                Question.max_level >= target_level,
            )
        )
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay preguntas cargadas todavía para este nivel",
        )
    return question


@router.get("/{skill_id}/history", response_model=list[SkillLevelLogRead])
async def get_skill_history(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    skill = await db.get(UserSkill, skill_id)
    if skill is None or skill.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill no encontrada")

    result = await db.scalars(
        select(SkillLevelLog)
        .where(SkillLevelLog.user_skill_id == skill_id)
        .order_by(SkillLevelLog.recorded_at)
    )
    return result.all()


@router.post("", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
async def create_custom_skill(
    payload: SkillCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    custom_skills = await db.scalars(
        select(UserSkill).where(
            UserSkill.user_id == current_user.id,
            UserSkill.is_core.is_(False),
        )
    )
    if len(custom_skills.all()) >= 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya tenés el máximo de 2 skills personalizadas",
        )

    skill = UserSkill(
        user_id=current_user.id, name=payload.name, is_core=False, level=1
    )
    db.add(skill)
    await db.commit()
    await db.refresh(skill)
    return skill


@router.patch("/{skill_id}/level", response_model=SkillRead)
async def level_up_skill(
    skill_id: int,
    payload: LevelUpRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    skill = await db.get(UserSkill, skill_id)
    if skill is None or skill.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill no encontrada")

    target_level = skill.level + 1

    attempt = LevelUpAttempt(
        user_skill_id=skill.id,
        question_id=payload.question_id,
        target_level=target_level,
        answer_text=payload.answer_text,
        self_confirmed=payload.self_confirmed,
    )
    db.add(attempt)

    if payload.self_confirmed:
        skill.level = target_level
        db.add(SkillLevelLog(user_skill_id=skill.id, level=target_level))

    await db.commit()
    await db.refresh(skill)
    return skill
