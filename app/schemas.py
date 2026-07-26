from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SkillCreate(BaseModel):
    name: str


class SkillRead(BaseModel):
    id: int
    name: str
    is_core: bool
    level: int

    model_config = ConfigDict(from_attributes=True)


class QuestionRead(BaseModel):
    id: int
    skill_name: str | None
    min_level: int
    max_level: int
    prompt: str

    model_config = ConfigDict(from_attributes=True)


class LevelUpRequest(BaseModel):
    question_id: int
    answer_text: str
    self_confirmed: bool


class SkillLevelLogRead(BaseModel):
    level: int
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SkillCardRead(BaseModel):
    id: int
    name: str
    is_core: bool
    level: int
    rarity: str


class ReferenceCardSkillRead(BaseModel):
    name: str
    is_core: bool
    level: int
    rarity: str


class ReferenceCardRead(BaseModel):
    id: int
    name: str
    photo_url: str
    description: str
    overall_rarity: str
    role: str
    skills: list[ReferenceCardSkillRead]
