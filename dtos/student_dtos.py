from typing import Optional
from pydantic import BaseModel, EmailStr


class StudentBaseDTO(BaseModel):
    nombres: str
    apellidos: str
    matricula: str
    promedio: float

class StudentCreateDTO(StudentBaseDTO):
    id: int
    class Config:
        from_attributes = True

class StudentUpdateDTO(BaseModel):
    matricula: Optional[str] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None

    class Config:
        from_attributes = True

class StudentResponseDTO(StudentBaseDTO):
    id: int
    class Config:
        from_attributes = True