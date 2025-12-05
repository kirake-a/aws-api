from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

import uuid

Base = declarative_base()

class StudentSchema(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String(200), nullable=False)
    apellidos = Column(String(200), nullable=False)
    matricula = Column(String(20), unique=True, nullable=False)
    promedio = Column(Float, nullable=False)
    foto_perfil_url = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)

class ProfessorSchema(Base):
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombres = Column(String(200), nullable=False)
    apellidos = Column(String(200), nullable=False)
    numero_empleado = Column(Integer, unique=True, nullable=False)
    horas_clase = Column(Integer, nullable=False)