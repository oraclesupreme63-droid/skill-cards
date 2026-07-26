from datetime import datetime

from sqlalchemy import ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    skills: Mapped[list["UserSkill"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class UserSkill(Base):
    __tablename__ = "user_skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str]
    is_core: Mapped[bool] = mapped_column(default=False)
    level: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="skills")
    level_logs: Mapped[list["SkillLevelLog"]] = relationship(
        back_populates="user_skill", cascade="all, delete-orphan"
    )
    attempts: Mapped[list["LevelUpAttempt"]] = relationship(
        back_populates="user_skill", cascade="all, delete-orphan"
    )


class SkillLevelLog(Base):
    __tablename__ = "skill_level_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_skill_id: Mapped[int] = mapped_column(ForeignKey("user_skills.id"))
    level: Mapped[int]
    recorded_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_skill: Mapped["UserSkill"] = relationship(back_populates="level_logs")


class ReferenceCard(Base):
    __tablename__ = "reference_cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    photo_url: Mapped[str]
    description: Mapped[str] = mapped_column(Text)


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    skill_name: Mapped[str | None] = mapped_column(default=None)
    min_level: Mapped[int] = mapped_column(default=1)
    max_level: Mapped[int] = mapped_column(default=100)
    prompt: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    attempts: Mapped[list["LevelUpAttempt"]] = relationship(back_populates="question")


class LevelUpAttempt(Base):
    __tablename__ = "level_up_attempts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_skill_id: Mapped[int] = mapped_column(ForeignKey("user_skills.id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    target_level: Mapped[int]
    answer_text: Mapped[str] = mapped_column(Text)
    self_confirmed: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user_skill: Mapped["UserSkill"] = relationship(back_populates="attempts")
    question: Mapped["Question"] = relationship(back_populates="attempts")
