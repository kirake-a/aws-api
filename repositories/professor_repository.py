from typing import List
from models.professor import Professor

class ProfessorRepository:
    def __init__(self):
        self.professor_data: List[Professor] = []

    def get_all_professors(self) -> List[Professor]:
        return self.professor_data

    def get_professor_by_id(self, professor_id: int) -> Professor | None:
        for professor in self.professor_data:
            if professor.id == professor_id:
                return professor

        return None

    def create_professor(self, professor: Professor) -> Professor:
        self.professor_data.append(professor)

        return professor

    def update_professor(self, professor_id: int, updated_professor: Professor) -> Professor | None:
        for index, professor in enumerate(self.professor_data):
            if professor.id == professor_id:
                self.professor_data[index] = updated_professor
                return updated_professor

        return None

    def delete_professor(self, professor_id: int) -> Professor | None:
        for index, professor in enumerate(self.professor_data):
            if professor.id == professor_id:
                del self.professor_data[index]
                return professor

        return None

    def is_professor_exist(self, professor_id: int) -> bool:
        for professor in self.professor_data:
            if professor.id == professor_id:
                return True
        return False