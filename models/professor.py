from dataclasses import dataclass

@dataclass
class Professor:
    id: str
    employee_number: str
    name: str
    last_name: str
    email: str
    class_hours: int