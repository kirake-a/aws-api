from typing import Optional
from pydantic import BaseModel, EmailStr


class ProfessorBaseDTO(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    class_hours: int

class ProfessorCreateDTO(ProfessorBaseDTO):
    class Config:
        from_attributes = True

class ProfessorUpdateDTO(BaseModel):
    employee_number: Optional[str] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    class_hours: Optional[int] = None

    class Config:
        from_attributes = True

class ProfessorResponseDTO(ProfessorBaseDTO):
    id: str
    employee_number: str

    class Config:
        from_attributes = True