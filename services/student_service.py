from typing import List
from config.logger_config import setup_logger
from repositories.student_repository import StudentRepository
from dtos.student_dtos import StudentCreateDTO, StudentUpdateDTO
from exceptions.cannot_delete_resource_exception import CannotDeleteResourceException
from exceptions.cannot_update_resource_exception import CannotUpdateResourceException
from exceptions.conflict_with_existing_resources_exception import ConflictWithExistingResourcesException
from exceptions.resource_not_found_exception import ResourceNotFoundException
from interfaces.service_interface import ServiceInterface
from models.student import Student
from utils.constants import STUDENT_NOT_FOUND
from utils.email_exist import email_exists
from utils.id_factory import generate_id, generate_registration


class StudentService(ServiceInterface):
    def __init__(self):
        self.repository = StudentRepository()
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
        student_dict = student_data.model_dump()

        if student_data.promedio < 0.0 or student_data.promedio > 10.0:
            self.logger.error("Invalid average score provided")
            raise ConflictWithExistingResourcesException("Average score must be between 0.0 and 10.0")

        new_student = Student(**student_dict)
        student = self.repository.create_student(new_student)

        self.logger.info(f"Student created with ID: {student.id}")
        return student

    def update(self, student_id: int, student_data: StudentUpdateDTO) -> Student:
        self.logger.info("Starting update process")
        existing_student = self.repository.get_student_by_id(student_id)

        if not existing_student:
            self.logger.error(f"Student with ID: {student_id} not found")
            raise ResourceNotFoundException(STUDENT_NOT_FOUND + " while updating")
        
        updated_data = student_data.model_dump(exclude_unset=True)

        for key, value in updated_data.items():
            setattr(existing_student, key, value)
        
        updated_student = self.repository.update_student(student_id, existing_student)

        if updated_student is not None:
            self.logger.info(f"Student with ID: {updated_student.id} updated successfully")
            return updated_student
        
        self.logger.error(f"Could not update student with ID: {student_id}")
        raise CannotUpdateResourceException("Could not update student")

    def delete(self, student_id: str) -> None:
        if not self.repository.exist(student_id):
            self.logger.error(f"Student with ID: {student_id} not found")
            raise ResourceNotFoundException(STUDENT_NOT_FOUND + " while deleting")

        self.logger.info(f"Attempt to delete student with ID: {student_id}")
        student = self.repository.delete_student(student_id)

        if student is None:
            self.logger.error(f"Could not delete student with ID: {student_id}")
            raise CannotDeleteResourceException("Could not delete student")
