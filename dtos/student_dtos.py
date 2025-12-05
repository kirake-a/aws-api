from typing import Optional
from pydantic import BaseModel


class StudentBaseDTO(BaseModel):
    nombres: str
    apellidos: str
    matricula: str
    promedio: float

class StudentCreateDTO(StudentBaseDTO):
    password: str

    class Config:
        from_attributes = True

class StudentUpdateDTO(BaseModel):
    matricula: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    promedio: Optional[float] = None

    class Config:
        from_attributes = True

class StudentResponseDTO(StudentBaseDTO):
    id: str
    
    class Config:
        from_attributes = True