from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import SessionLocal

router = APIRouter()

@router.get("/challenges")
async def get_challenges():
    """
    Obtener todos los retos (challenges).
    """
    session: Session = SessionLocal()
    result = session.execute("SELECT * FROM challenges").fetchall()
    session.close()
    return {"data": [dict(row) for row in result]}
