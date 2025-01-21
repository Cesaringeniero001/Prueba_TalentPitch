from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import SessionLocal

router = APIRouter()

@router.get("/profiles")
async def get_profiles():
    """
    Obtener todos los perfiles (profiles).
    """
    session: Session = SessionLocal()
    result = session.execute("SELECT * FROM profiles").fetchall()
    session.close()
    return {"data": [dict(row) for row in result]}
