from typing import List
from db.schemas import StudentSchema
from models.student import Student
from mappers.student_mapper import map_model_to_schema, map_schema_to_model

from sqlalchemy.orm import Session


class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_students(self) -> List[Student]:
        students_schema = self.db.query(StudentSchema).all()

        students = [map_schema_to_model(student_schema) for student_schema in students_schema]

        return students

    def get_student_by_id(self, student_id: str) -> Student | None:
        student_schema = self.db.query(StudentSchema).filter(StudentSchema.id == student_id).first()
        
        if not student_schema:
            return None

        return map_schema_to_model(student_schema)

    def create_student(self, student: Student) -> Student:
        student_schema = map_model_to_schema(student)
        
        self.db.add(student_schema)
        self.db.commit()
        self.db.refresh(student_schema)

        return map_schema_to_model(student_schema)

    def update_student(self, student_id: str, updated_student: dict) -> Student | None:
        student_schema = self.db.query(StudentSchema).filter(StudentSchema.id == student_id).first()

        if not student_schema:
            return None
        
        for key, value in updated_student.items():
            if (hasattr(student_schema, key)):
                setattr(student_schema, key, value)

        self.db.commit()
        self.db.refresh(student_schema)

        return map_schema_to_model(student_schema)

    def delete_student(self, student_id: str) -> bool:
        student_deleted = self.db.query(StudentSchema).filter(StudentSchema.id == student_id).delete()
        
        self.db.commit()

        return student_deleted > 0

    def exist(self, student_id: str) -> bool:
        exits_student = self.db.query(StudentSchema).filter(StudentSchema.id == student_id).first()

        return exits_student is not None