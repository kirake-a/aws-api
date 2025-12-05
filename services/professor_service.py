from typing import List

from sqlalchemy.orm import Session

from config.logger_config import setup_logger
from exceptions.invalid_argument_exception import InvalidArgumentException
from mappers.professor_mapper import create_professor_dto_to_model
from repositories.professor_repository import ProfessorRepository
from dtos.professor_dtos import ProfessorCreateDTO, ProfessorUpdateDTO
from exceptions.cannot_delete_resource_exception import CannotDeleteResourceException
from exceptions.cannot_update_resource_exception import CannotUpdateResourceException
from exceptions.resource_not_found_exception import ResourceNotFoundException
from interfaces.service_interface import ServiceInterface
from models.professor import Professor
from utils.constants import PROFESSOR_NOT_FOUND


class ProfessorService(ServiceInterface):
    def __init__(self, db: Session):
        self.repository = ProfessorRepository(db)
        self.logger = setup_logger(self.__class__.__name__)

    def get_all(self) -> List[Professor]:
        self.logger.info("Fetching all professors from the repository")
        return self.repository.get_all_professors()

    def get_by_id(self, professor_id: int) -> Professor:
        self.logger.info(f"Fetching professor with ID: {professor_id}")
        professor = self.repository.get_professor_by_id(professor_id)

        if professor is not None:
            return professor
        
        self.logger.error(f"Professor with ID: {professor_id} not found")
        raise ResourceNotFoundException(PROFESSOR_NOT_FOUND)

    def create(self, professor_data: ProfessorCreateDTO) -> Professor:
        self.logger.info("Creating a new professor")

        if professor_data.horasClase < 0 or professor_data.horasClase > 100:
            self.logger.error("Invalid class hours provided")
            raise InvalidArgumentException("Class hours must be between 0 and 100")
        
        if professor_data.numeroEmpleado <= 0:
            self.logger.error("Invalid employee number provided")
            raise InvalidArgumentException("Employee number must be a positive integer")

        new_professor = create_professor_dto_to_model(professor_data)

        professor = self.repository.create_professor(new_professor)

        self.logger.info(f"Professor created with ID: {professor.id}")
        return professor

    def update(self, professor_id: int, professor_data: ProfessorUpdateDTO) -> Professor:
        existing_professor = self.repository.get_professor_by_id(professor_id)

        if not existing_professor:
            self.logger.error(f"Professor with ID: {professor_id} not found")
            raise ResourceNotFoundException(PROFESSOR_NOT_FOUND)
        
        updated_data = professor_data.model_dump(exclude_unset=True, by_alias=True)
        
        updated_professor = self.repository.update_professor(professor_id, updated_data)

        if updated_professor is not None:
            self.logger.info(f"Professor with ID: {updated_professor.id} updated successfully")
            return updated_professor
        
        self.logger.error(f"Could not update professor with ID: {professor_id}")
        raise CannotUpdateResourceException("Could not update professor")

    def delete(self, professor_id: int) -> None:
        if not self.repository.is_professor_exist(professor_id):
            self.logger.error(f"Professor with ID: {professor_id} not found")
            raise ResourceNotFoundException(PROFESSOR_NOT_FOUND)
        
        self.logger.info(f"Attempt to delete professor with ID: {professor_id}")
        professor = self.repository.delete_professor(professor_id)

        if professor is None:
            self.logger.error(f"Could not delete professor with ID: {professor_id}")
            raise CannotDeleteResourceException("Could not delete professor")