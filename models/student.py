from dataclasses import dataclass

@dataclass
class Student:
    id: str
    nombres: str
    apellidos: str
    matricula: str
    promedio: float
    foto_perfil_url: str | None
    password: str