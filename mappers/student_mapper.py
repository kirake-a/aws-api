from dtos.student_dtos import StudentCreateDTO
from models.student import Student
from db.schemas import StudentSchema

def create_student_dto_to_model(
        dto: StudentCreateDTO,
        hashed_pwd: str
) -> Student:
    return Student(
        id=None,
        nombres=dto.nombres,
        apellidos=dto.apellidos,
        matricula=dto.matricula,
        promedio=dto.promedio,
        foto_perfil_url=None,
        password=hashed_pwd
    )

def map_model_to_schema(model: Student) -> StudentSchema:
    return StudentSchema(
        id=model.id,
        nombres=model.nombres,
        apellidos=model.apellidos,
        matricula=model.matricula,
        promedio=model.promedio,
        foto_perfil_url=model.foto_perfil_url,
        password=model.password
    )

def map_schema_to_model(schema: StudentSchema) -> Student:
    return Student(
        id=schema.id,
        nombres=schema.nombres,
        apellidos=schema.apellidos,
        matricula=schema.matricula,
        promedio=schema.promedio,
        foto_perfil_url=schema.foto_perfil_url,
        password=schema.password
    )