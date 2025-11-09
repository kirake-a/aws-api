from typing import Optional
from pydantic import BaseModel, EmailStr


class StudentBaseDTO(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    semester: int
    average_grade: float

class StudentCreateDTO(StudentBaseDTO):
    class Config:
        from_attributes = True

class StudentUpdateDTO(BaseModel):
    registration: Optional[str] = None
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    semester: Optional[int] = None
    average_grade: Optional[float] = None

    class Config:
        from_attributes = True

class StudentResponseDTO(StudentBaseDTO):
    id: str
    registration: str

    class Config:
        from_attributes = True