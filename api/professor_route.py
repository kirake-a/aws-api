from typing import List
from fastapi import APIRouter, status

from dtos.professor_dtos import ProfessorCreateDTO, ProfessorResponseDTO, ProfessorUpdateDTO
from dtos.response_wrapper import ResponseWrapper
from services.professor_service import ProfessorService

router = APIRouter(prefix="/profesores", tags=["Profesores"])

service = ProfessorService()

@router.get(
    "/",
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
        data=[ProfessorResponseDTO.model_validate(professor) for professor in professors]
    )

@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseWrapper[ProfessorResponseDTO],
    summary="Get professor by ID",
    description="Retrieve a professor by their unique ID."
)
async def get_professor_by_id(id: str) -> ResponseWrapper[ProfessorResponseDTO]:
    professor = service.get_by_id(id)

    return ResponseWrapper(
        success=True,
        message="Professor retrieved successfully.",
        data=ProfessorResponseDTO.model_validate(professor)
    )

@router.post(
    "/",
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
        data=ProfessorResponseDTO.model_validate(created_professor)
    )

@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseWrapper[ProfessorResponseDTO],
    summary="Update a professor",
    description="Update an existing professor in the system."
)
async def update_professor(id: str, professor: ProfessorUpdateDTO) -> ResponseWrapper[ProfessorResponseDTO]:
    updated_professor = service.update(id, professor)

    return ResponseWrapper(
        success=True,
        message=f"Professor {updated_professor.name + ' ' + updated_professor.last_name} updated successfully.",
        data=ProfessorResponseDTO.model_validate(updated_professor)
    )

@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a professor",
    description="Delete an existing professor from the system."
)
async def delete_professor(id: str):
    service.delete(id)