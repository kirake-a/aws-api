from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

import uuid

Base = declarative_base()

class StudentSchema(Base):
    __tablename__ = "students"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    matricula = Column(String, unique=True, nullable=False)
    promedio = Column(Float, nullable=False)
    foto_perfil_url = Column(String, nullable=True)
    password = Column(String, nullable=False)

class ProfessorSchema(Base):
    __tablename__ = "professors"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    nombres = Column(String, nullable=False)
    apellidos = Column(String, nullable=False)
    numero_empleado = Column(Integer, unique=True, nullable=False)
    horas_clase = Column(Integer, nullable=False)