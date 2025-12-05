from dataclasses import dataclass

@dataclass
class Professor:
    id: int
    numero_empleado: int
    nombres: str
    apellidos: str
    horas_clase: int