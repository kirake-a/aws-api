from typing import List
from models.student import Student


class StudentRepository:
    def __init__(self):
        self.student_data: List[Student] = []

    def get_all_students(self) -> List[Student]:
        return self.student_data

    def get_student_by_id(self, student_id: int) -> Student | None:
        for student in self.student_data:
            if student.id == student_id:
                return student

        return None

    def create_student(self, student: Student) -> Student:
        self.student_data.append(student)

        return student

    def update_student(self, student_id: int, updated_student: Student) -> Student | None:
        for index, student in enumerate(self.student_data):
            if student.id == student_id:
                self.student_data[index] = updated_student
                return updated_student

        return None

    def delete_student(self, student_id: str) -> Student | None:
        for index, student in enumerate(self.student_data):
            if student.id == student_id:
                del self.student_data[index]
                return student

        return None

    def exist(self, student_id: str) -> bool:
        for student in self.student_data:
            if student.id == student_id:
                return True
        return False