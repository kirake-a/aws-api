from typing import Optional
from pydantic import BaseModel, Field


class ProfessorBaseDTO(BaseModel):
    nombres: str
    apellidos: str
    numeroEmpleado: int
    horasClase: int

class ProfessorCreateDTO(ProfessorBaseDTO):
    
    class Config:
        from_attributes = True

class ProfessorUpdateDTO(BaseModel):
    numeroEmpleado: Optional[int] = Field(None, alias='numero_empleado')
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    horasClase: Optional[int] = Field(None, alias='horas_clase')

    class Config:
        from_attributes = True
        populate_by_name = True

class ProfessorResponseDTO(ProfessorBaseDTO):
    id: int

    class Config:
        from_attributes = True