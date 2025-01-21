from fastapi import FastAPI, UploadFile, HTTPException
from app.routes import challenges, profiles, users, resumes
from app.database import engine
from app.models import Base
from app.utils import process_csv_batch

# Se crean las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Instancia de API
app = FastAPI(title="Data Migration API")

# Registrar los routers
app.include_router(challenges.router, prefix="/api/challenges", tags=["Challenges"])
app.include_router(profiles.router, prefix="/api/profiles", tags=["Profiles"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(resumes.router, prefix="/api/resumes", tags=["Resumes"])

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Migración de Datos"}



@app.post("/upload/{table_name}")
async def upload_csv(table_name: str, file: UploadFile):
    """
    Endpoint para cargar un archivo CSV y migrar los datos a la tabla especificada.
    """

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV.")

    try:
        rows_inserted = process_csv_batch(file.file, table_name)
        return {"message": f"Se migraron {rows_inserted} filas a la tabla {table_name}."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
