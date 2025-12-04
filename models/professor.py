from dataclasses import dataclass

@dataclass
class Professor:
    id: str
    numero_empleado: int
    nombres: str
    apellidos: str
    horas_clase: int