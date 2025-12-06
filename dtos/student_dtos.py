from typing import Optional
from pydantic import BaseModel, Field


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
    id: int
    fotoPerfilUrl: Optional[str] = Field(None, validation_alias="foto_perfil_url")
    
    class Config:
        from_attributes = True
        populate_by_name = True

class StudentLoginDTO(BaseModel):
    password: str

    class Config:
        from_attributes = True

class ValidateStudentDTO(BaseModel):
    sessionString: str = Field(..., alias="session_string")

    class Config:
        from_attributes = True
        populate_by_name = True

class SessionResponseDTO(BaseModel):
    sessionString: str

    class Config:
        from_attributes = True