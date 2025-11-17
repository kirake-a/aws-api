from typing import List
from fastapi import APIRouter, status

from dtos import StudentCreateDTO, StudentResponseDTO, StudentUpdateDTO, ResponseWrapper
from services.student_service import StudentService

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])

service = StudentService()

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ResponseWrapper[List[StudentResponseDTO]],
    summary="Get all students",
    description="Retrieve a list of all students in the system."
)
async def get_all_students() -> ResponseWrapper[List[StudentResponseDTO]]:
    students = service.get_all()

    return ResponseWrapper(
        success=True,
        message="Students retrieved successfully.",
        data=[StudentResponseDTO.model_validate(student) for student in students]
    )

@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=StudentResponseDTO,
    summary="Get student by ID",
    description="Retrieve a student by their unique ID. Validates that the ID exists."
)
async def get_student_by_id(id: int) -> ResponseWrapper[StudentResponseDTO]:
    student = service.get_by_id(id)

    return StudentResponseDTO.model_validate(student)

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseWrapper[StudentResponseDTO],
    summary="Create a new student",
    description="Create a new student in the system."
)
async def create_student(student: StudentCreateDTO) -> ResponseWrapper[StudentResponseDTO]:
    create_student = service.create(student)

    return ResponseWrapper(
        success=True,
        message="Student created successfully.",
        data=StudentResponseDTO.model_validate(create_student),
        status_code=status.HTTP_201_CREATED
    )

@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseWrapper[StudentResponseDTO],
    summary="Update an existing student",
    description="Update an existing student in the system."
)
async def update_student(id: int, student: StudentUpdateDTO) -> ResponseWrapper[StudentResponseDTO]:
    updated_student = service.update(id, student)

    return ResponseWrapper(
        success=True,
        message="Student updated successfully.",
        data=StudentResponseDTO.model_validate(updated_student)
    )

@router.delete(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a student",
    description="Delete an existing student from the system."
)
async def delete_student(id: int):
    service.delete(id)