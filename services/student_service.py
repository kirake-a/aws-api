from fastapi import UploadFile

from typing import List

from sqlalchemy.orm import Session

from config.logger_config import setup_logger
from exceptions.invalid_argument_exception import InvalidArgumentException
from mappers.student_mapper import create_student_dto_to_model
from repositories.student_repository import StudentRepository
from dtos.student_dtos import StudentCreateDTO, StudentUpdateDTO
from exceptions.cannot_delete_resource_exception import CannotDeleteResourceException
from exceptions.cannot_update_resource_exception import CannotUpdateResourceException
from exceptions.conflict_with_existing_resources_exception import ConflictWithExistingResourcesException
from exceptions.resource_not_found_exception import ResourceNotFoundException
from interfaces.service_interface import ServiceInterface
from models.student import Student
from services.dynamo_service import DynamoDBService
from services.s3_service import S3Service
from services.sns_service import SNSService
from utils.constants import STUDENT_NOT_FOUND
from utils.id_factory import (
    get_password_hash,
    verify_password,
    generate_session_string
)


class StudentService(ServiceInterface):
    def __init__(self, db: Session):
        self.repository = StudentRepository(db)
        self.s3_service = S3Service()
        self.dynamo_service = DynamoDBService()
        self.sns_service = SNSService()
        self.logger = setup_logger(self.__class__.__name__)
        
    def get_all(self) -> List[Student]:
        self.logger.info("Fetching all students from the repository")
        return self.repository.get_all_students()

    def get_by_id(self, student_id: int) -> Student:
        self.logger.info(f"Fetching student with ID: {student_id}")
        student = self.repository.get_student_by_id(student_id)

        if student is not None:
            self.logger.info(f"Student with ID: {student_id} found")
            return student
        
        self.logger.error(f"Student with ID: {student_id} not found")
        raise ResourceNotFoundException(STUDENT_NOT_FOUND)

    def create(self, student_data: StudentCreateDTO) -> Student:

        if student_data.promedio < 0.0 or student_data.promedio > 10.0:
            self.logger.error("Invalid average score provided")
            raise InvalidArgumentException("Average score must be between 0.0 and 10.0")

        raw_password = student_data.password
        if not raw_password:
            self.logger.error("Password cannot be empty")
            raise InvalidArgumentException("Password cannot be empty")
            
        hashed_pwd = get_password_hash(raw_password)
        new_student = create_student_dto_to_model(student_data, hashed_pwd)
        student = self.repository.create_student(new_student)

        self.logger.info(f"Student created with ID: {student.id}")
        return student

    def update(self, student_id: int, student_data: StudentUpdateDTO) -> Student:
        self.logger.info("Starting update process")
        if student_data.promedio is not None:
            if student_data.promedio < 0.0 or student_data.promedio > 10.0:
                self.logger.error("Invalid average score provided")
                raise InvalidArgumentException("Average score must be between 0.0 and 10.0")
            
        updated_data = student_data.model_dump(exclude_unset=True)

        updated_student = self.repository.update_student(student_id, updated_data)

        if updated_student is not None:
            self.logger.info(f"Student with ID: {updated_student.id} updated successfully")
            return updated_student
        
        self.logger.error(f"Could not update student with ID: {student_id}")
        raise CannotUpdateResourceException("Could not update student")

    def delete(self, student_id: int) -> None:
        self.logger.info(f"Attempt to delete student with ID: {student_id}")
        was_student = self.repository.delete_student(student_id)

        if not was_student:
            self.logger.error(f"Could not delete student with ID: {student_id}")
            raise CannotDeleteResourceException("Could not delete student")
        
        self.logger.info(f"Student with ID: {student_id} deleted successfully")

    def upload_profile_picture(self, student_id: int, file: UploadFile) -> Student:
        self.logger.info(f"Uploading profile picture for student ID: {student_id}")

        student = self.repository.get_student_by_id(student_id)

        if not student:
            self.logger.error(f"Student with ID: {student_id} not found")
            raise ResourceNotFoundException(STUDENT_NOT_FOUND)
        
        file_extension = file.filename.split(".")[-1]
        file_name = f"profiles/students/{student_id}.{file_extension}"

        url = self.s3_service.upload_file(file, file_name)

        updated_student = self.repository.update_student(
            student_id,
            {"foto_perfil_url": url}
        )

        return updated_student
    
    def login(
        self,
        student_id: int,
        password: str
    ) -> str:
        self.logger.info(f"Attempt to login with student ID: {student_id}")
        student = self.repository.get_student_by_id(student_id)

        if not student:
            self.logger.error(f"Student with ID: {student_id} not found")
            raise ResourceNotFoundException(STUDENT_NOT_FOUND)
        
        if not verify_password(password, student.password):
            self.logger.error("Invalid password provided")
            raise InvalidArgumentException("Invalid password")
        
        session_string = generate_session_string()
        self.dynamo_service.create_session(student_id, session_string)

        self.logger.info(f"Student with ID: {student_id} logged in successfully")
        return session_string

    def validate_session(
        self,
        student_id: int,
        session_string: str
    ) -> bool:
        self.logger.info(f"Validating session for student ID: {student_id}")

        session = self.dynamo_service.get_session_by_string(session_string)

        if not session:
            return False
        
        if int(session['alumnoId']) != student_id:
            return False
        
        if not session['active']:
            return False
        
        self.logger.info(f"Session for student ID: {student_id} is valid")
        return True

    def logout(
        self,
        student_id: int,
        session_string: str
    ):
        self.logger.info(f"Attempt to logout student ID: {student_id}")

        session = self.dynamo_service.get_session_by_string(session_string)

        if session and int(session.get('alumnoId')) == student_id:
            self.dynamo_service.invalidate_session(session['id'])
            self.logger.info(f"Student with ID: {student_id} logged out successfully")

    def send_student_info_email(self, student_id: int):
        self.logger.info(f"Preparing to send email info for student ID: {student_id}")

        student = self.repository.get_student_by_id(student_id)
        if not student:
            raise ResourceNotFoundException(STUDENT_NOT_FOUND)

        subject = f"Información Académica: {student.nombres} {student.apellidos}"
        
        message = (
            f"Hola,\n\n"
            f"Se ha solicitado la información del siguiente alumno:\n"
            f"---------------------------------------------------\n"
            f"ID: {student.id}\n"
            f"Nombre: {student.nombres} {student.apellidos}\n"
            f"Matrícula: {student.matricula}\n"
            f"Promedio General: {student.promedio}\n"
            f"---------------------------------------------------\n"
            f"Saludos,\nSistema de Alumnos AWS API"
        )

        self.sns_service.publish_message(subject, message)
        
        self.logger.info("Email notification sent via SNS successfully")
