from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import SessionLocal

router = APIRouter()

@router.get("/resumes")
async def get_resumes():
    """
    Obtener todos los currículos (resumes).
    """
    session: Session = SessionLocal()
    result = session.execute("SELECT * FROM resumes").fetchall()
    session.close()
    return {"data": [dict(row) for row in result]}
