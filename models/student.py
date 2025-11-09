from dataclasses import dataclass

@dataclass
class Student:
    id: str
    registration: str
    name: str
    last_name: str
    email: str
    semester: int
    average_grade: float