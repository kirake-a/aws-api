from typing import List
from config.logger_config import setup_logger
from db.professor_repository import ProfessorRepository
from dtos.professor_dtos import ProfessorCreateDTO, ProfessorUpdateDTO
from exceptions.cannot_delete_resource_exception import CannotDeleteResourceException
from exceptions.cannot_update_resource_exception import CannotUpdateResourceException
from exceptions.conflict_with_existing_resources_exception import ConflictWithExistingResourcesException
from exceptions.resource_not_found_exception import ResourceNotFoundException
from interfaces.service_interface import ServiceInterface
from models.professor import Professor
from utils.constants import PROFESSOR_NOT_FOUND
from utils.email_exist import email_exists
from utils.id_factory import generate_employee_number, generate_id


class ProfessorService(ServiceInterface):
    def __init__(self):
        self.repository = ProfessorRepository()
        self.logger = setup_logger(self.__class__.__name__)

    def get_all(self) -> List[Professor]:
        self.logger.info("Fetching all professors from the repository")
        return self.repository.get_all_professors()

    def get_by_id(self, professor_id: str) -> Professor:
        self.logger.info(f"Fetching professor with ID: {professor_id}")
        professor = self.repository.get_professor_by_id(professor_id)

        if professor is not None:
            return professor
        
        self.logger.error(f"Professor with ID: {professor_id} not found")
        raise ResourceNotFoundException(PROFESSOR_NOT_FOUND)

    def create(self, professor_data: ProfessorCreateDTO) -> Professor:
        self.logger.info(f"Creating new professor with email: {professor_data.email}")

        if email_exists(professor_data.email, self.repository.get_all_professors()):
            self.logger.error(f"Email already exists: {professor_data.email}")
            raise ConflictWithExistingResourcesException("Email already exists")
        
        professor_id = generate_id()
        professor_employee_number = generate_employee_number()
        professor_dict = professor_data.model_dump()

        new_professor = Professor(id=professor_id, employee_number=professor_employee_number, **professor_dict)

        professor = self.repository.create_professor(new_professor)

        self.logger.info(f"Professor created with ID: {professor_id}")
        return professor

    def update(self, professor_id: str, professor_data: ProfessorUpdateDTO) -> Professor:
        existing_professor = self.repository.get_professor_by_id(professor_id)

        if not existing_professor:
            self.logger.error(f"Professor with ID: {professor_id} not found")
            raise ResourceNotFoundException(PROFESSOR_NOT_FOUND)
        
        updated_data = professor_data.model_dump(exclude_unset=True)

        for key, value in updated_data.items():
            setattr(existing_professor, key, value)
        
        updated_professor = self.repository.update_professor(professor_id, existing_professor)

        if updated_professor is not None:
            self.logger.info(f"Professor with ID: {updated_professor.id} updated successfully")
            return updated_professor
        
        self.logger.error(f"Could not update professor with ID: {professor_id}")
        raise CannotUpdateResourceException("Could not update professor")

    def delete(self, professor_id: str) -> None:
        if not self.repository.is_professor_exist(professor_id):
            self.logger.error(f"Professor with ID: {professor_id} not found")
            raise ResourceNotFoundException(PROFESSOR_NOT_FOUND)
        
        self.logger.info(f"Attempt to delete professor with ID: {professor_id}")
        professor = self.repository.delete_professor(professor_id)

        if professor is None:
            self.logger.error(f"Could not delete professor with ID: {professor_id}")
            raise CannotDeleteResourceException("Could not delete professor")