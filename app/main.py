from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlalchemy import text

from app.auth.router import router as auth_router
from app.database import engine
from app.routers.cards import router as cards_router
from app.routers.skills import router as skills_router

app = FastAPI(title="Skill Cards API")
app.include_router(auth_router)
app.include_router(skills_router)
app.include_router(cards_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/health")
async def health():
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    return {"status": "ok"}
