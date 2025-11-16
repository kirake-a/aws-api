from dataclasses import dataclass

@dataclass
class Student:
    id: str
    nombres: str
    apellidos: str
    matricula: str
    promedio: float