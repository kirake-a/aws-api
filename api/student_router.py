from typing import List
from fastapi import APIRouter, Depends, status, UploadFile, File

from sqlalchemy.orm import Session

from db.database import get_db

from dtos import (
    StudentCreateDTO,
    StudentResponseDTO,
    StudentUpdateDTO,
    StudentLoginDTO,
    ValidateStudentDTO,
    ResponseWrapper
)
from services.student_service import StudentService

router = APIRouter(prefix="/alumnos", tags=["Alumnos"])

def get_student_service(db: Session = Depends(get_db)) -> StudentService:
    return StudentService(db)

@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ResponseWrapper[List[StudentResponseDTO]],
    summary="Get all students",
    description="Retrieve a list of all students in the system."
)
async def get_all_students(
    service: StudentService = Depends(get_student_service)
) -> ResponseWrapper[List[StudentResponseDTO]]:
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
async def get_student_by_id(
    id: int,
    service: StudentService = Depends(get_student_service)
) -> ResponseWrapper[StudentResponseDTO]:

    student = service.get_by_id(id)

    return StudentResponseDTO.model_validate(student)

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseWrapper[StudentResponseDTO],
    summary="Create a new student",
    description="Create a new student in the system."
)
async def create_student(
    student: StudentCreateDTO,
    service: StudentService = Depends(get_student_service)
) -> ResponseWrapper[StudentResponseDTO]:

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
async def update_student(
    id: int,
    student: StudentUpdateDTO,
    service: StudentService = Depends(get_student_service)
) -> ResponseWrapper[StudentResponseDTO]:

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
async def delete_student(
    id: int,
    service: StudentService = Depends(get_student_service)
):

    service.delete(id)

@router.post(
    "/{id}/fotoPerfil",
    status_code=status.HTTP_200_OK,
    response_model=ResponseWrapper[StudentResponseDTO],
    summary="Upload profile picture for a student",
    description="Upload a profile picture for the specified student."
)
async def upload_profile_picture(
    id: int,
    file: UploadFile = File(...),
    service: StudentService = Depends(get_student_service)
):
    updated_student = service.upload_profile_picture(id, file)

    return ResponseWrapper(
        success=True,
        message="Profile picture uploaded successfully.",
        data=StudentResponseDTO.model_validate(updated_student)
    )

@router.post(
    "/{id}/session/login",
    status_code=status.HTTP_200_OK,
    response_model=ResponseWrapper[str],
    summary="Student login",
    description="Authenticate a student and create a session."
)
async def session_login(
    id: int,
    data: StudentLoginDTO,
    service: StudentService = Depends(get_student_service)
):
    pass

@router.post(
    "/{id}/session/verify",
    status_code=status.HTTP_200_OK,
    response_model=ResponseWrapper[bool],
    summary="Verify student session",
    description="Verify if a student's session is still valid."
)
async def session_verify(
    id: int,
    session: ValidateStudentDTO,
    service: StudentService = Depends(get_student_service)
):
    pass

@router.post(
    "/{id}/session/logout",
    status_code=status.HTTP_200_OK,
    response_model=ResponseWrapper[None],
    summary="Student logout",
    description="Terminate a student's session."
)
async def session_logout(
    id: str,
    session: ValidateStudentDTO,
    service: StudentService = Depends(get_student_service)
):
    pass