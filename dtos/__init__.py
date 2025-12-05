from .student_dtos import (
    StudentCreateDTO,
    StudentResponseDTO,
    StudentUpdateDTO,
    StudentLoginDTO,
    ValidateStudentDTO
)
from .professor_dtos import (
    ProfessorCreateDTO,
    ProfessorResponseDTO,
    ProfessorUpdateDTO
)
from .response_wrapper import ResponseWrapper

__all__ = [
    "StudentCreateDTO",
    "StudentResponseDTO",
    "StudentUpdateDTO",
    "ProfessorCreateDTO",
    "ProfessorResponseDTO",
    "ProfessorUpdateDTO"
]
