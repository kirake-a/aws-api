from typing import List
from db.schemas import ProfessorSchema
from mappers.professor_mapper import map_schema_to_model, map_model_to_schema
from models.professor import Professor

from sqlalchemy.orm import Session

class ProfessorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_professors(self) -> List[Professor]:
        professors_schema = self.db.query(ProfessorSchema).all()

        professors = [map_schema_to_model(professor_schema) for professor_schema in professors_schema]
        
        return professors

    def get_professor_by_id(self, professor_id: int) -> Professor | None:
        student_schema = self.db.query(ProfessorSchema).filter(ProfessorSchema.id == professor_id).first()
        
        if not student_schema:
            return None
        
        return map_schema_to_model(student_schema)

    def create_professor(self, professor: Professor) -> Professor:
        student_schema = map_model_to_schema(professor)

        self.db.add(student_schema)
        self.db.commit()
        self.db.refresh(student_schema)

        return map_schema_to_model(student_schema)

    def update_professor(self, professor_id: int, updated_professor: dict) -> Professor | None:
        student_schema = self.db.query(ProfessorSchema).filter(ProfessorSchema.id == professor_id).first()

        if not student_schema:
            return None
        
        for key, value in updated_professor.items():
            if (hasattr(student_schema, key)):
                setattr(student_schema, key, value)

        self.db.commit()
        self.db.refresh(student_schema)

        return map_schema_to_model(student_schema)

    def delete_professor(self, professor_id: int) -> Professor | None:
        professor_deleted = self.db.query(ProfessorSchema).filter(ProfessorSchema.id == professor_id).delete()

        self.db.commit()

        return professor_deleted > 0

    def is_professor_exist(self, professor_id: int) -> bool:
        exists_professor = self.db.query(ProfessorSchema).filter(ProfessorSchema.id == professor_id).first()

        return exists_professor is not None