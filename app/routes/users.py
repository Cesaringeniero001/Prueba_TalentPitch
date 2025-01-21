from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.database import SessionLocal

router = APIRouter()

@router.get("/users")
async def get_users():
    """
    Obtener todos los usuarios (users).
    """
    session: Session = SessionLocal()
    result = session.execute("SELECT * FROM users").fetchall()
    session.close()
    return {"data": [dict(row) for row in result]}
