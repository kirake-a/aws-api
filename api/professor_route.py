from typing import List
from fastapi import APIRouter, status

from dtos.professor_dtos import ProfessorCreateDTO, ProfessorResponseDTO, ProfessorUpdateDTO
from dtos.response_wrapper import ResponseWrapper
from services.professor_service import ProfessorService

router = APIRouter(prefix="/profesores", tags=["Profesores"])

service = ProfessorService()

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ResponseWrapper[List[ProfessorResponseDTO]],
    summary="Get all professors",
    description="Retrieve a list of all professors in the system."
)
async def get_all_professors() -> ResponseWrapper[List[ProfessorResponseDTO]]:
    professors = service.get_all()

    return ResponseWrapper(
        success=True,
        message="Professors retrieved successfully.",
        data=[ProfessorResponseDTO(
            id=professor.id,
            nombres=professor.nombres,
            apellidos=professor.apellidos,
            numeroEmpleado=professor.numero_empleado,
            horasClase=professor.horas_clase
        ) for professor in professors]
    )

@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ProfessorResponseDTO,
    summary="Get professor by ID",
    description="Retrieve a professor by their unique ID."
)
async def get_professor_by_id(id: int) -> ProfessorResponseDTO:
    professor = service.get_by_id(id)

    return ProfessorResponseDTO(
        id=professor.id,
        nombres=professor.nombres,
        apellidos=professor.apellidos,
        numeroEmpleado=professor.numero_empleado,
        horasClase=professor.horas_clase
    )

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseWrapper[ProfessorResponseDTO],
    summary="Create a new professor",
    description="Create a new professor in the system."
)
async def create_professor(professor: ProfessorCreateDTO) -> ResponseWrapper[ProfessorResponseDTO]:
    created_professor = service.create(professor)

    return ResponseWrapper(
        success=True,
        message="Professor created successfully.",
        data= ProfessorResponseDTO(
            id=created_professor.id,
            nombres=created_professor.nombres,
            apellidos=created_professor.apellidos,
            numeroEmpleado=created_professor.numero_empleado,
            horasClase=created_professor.horas_clase
        )
    )

@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseWrapper[ProfessorResponseDTO],
    summary="Update a professor",
    description="Update an existing professor in the system."
)
async def update_professor(id: int, professor: ProfessorUpdateDTO) -> ResponseWrapper[ProfessorResponseDTO]:
    updated_professor = service.update(id, professor)

    return ResponseWrapper(
        success=True,
        message=f"Professor {updated_professor.nombres + ' ' + updated_professor.apellidos} updated successfully.",
        data=ProfessorResponseDTO(
            id=updated_professor.id,
            nombres=updated_professor.nombres,
            apellidos=updated_professor.apellidos,
            numeroEmpleado=updated_professor.numero_empleado,
            horasClase=updated_professor.horas_clase
        )
    )

@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a professor",
    description="Delete an existing professor from the system."
)
async def delete_professor(id: int):
    service.delete(id)