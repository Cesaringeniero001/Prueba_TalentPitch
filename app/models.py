from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Las varibales 'user_id' en las tablas profile y resumes podrían ser Foreign Key que relacionan 'id' en 'users',
# sin embargo hay valores de id_user en las tablas 'profile' y 'resumes' que no están en 'users',
# no sería buena práctica migrar los datos como están, se podría omitir esta restricción(de sqalchemy), sin embargo, vamos simplemente a migrar
# los datos sin definir a 'user_id' como Foreign Key, estas modificaciones se pueden hacer en la nueva base de datos y decidir si
# eliminar  o añadir registros en las tablas en mención para un correcta dinámica en la base de datos relacional. 

class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    opencall_objective = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False)

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False) 
    onboarding_goal = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    views = Column(Integer, nullable=False)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    video = Column(String(255), nullable=True)
    identification_number = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False, unique=True)
    gender = Column(String(10), nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,  nullable=False)
    name = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)
    video = Column(String(150), nullable=False)  
    views = Column(Integer, nullable=False)  
    created_at = Column(DateTime, nullable=False)

