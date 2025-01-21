from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# configuraciones globales
DATABASE_URL = os.getenv("DATABASE_URL")
BATCH_SIZE = int(os.getenv("BATCH_SIZE"))
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1"]
