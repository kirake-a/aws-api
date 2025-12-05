from dtos.professor_dtos import ProfessorCreateDTO
from models.professor import Professor
from db.schemas import ProfessorSchema


def create_professor_dto_to_model(dto: ProfessorCreateDTO) -> Professor:
    return Professor(
        id=None,
        nombres=dto.nombres,
        apellidos=dto.apellidos,
        numero_empleado=dto.numeroEmpleado,
        horas_clase=dto.horasClase
    )
    
def map_model_to_schema(model: Professor) -> ProfessorSchema:
    return ProfessorSchema(
        id=model.id,
        nombres=model.nombres,
        apellidos=model.apellidos,
        numero_empleado=model.numero_empleado,
        horas_clase=model.horas_clase
    )
    
def map_schema_to_model(schema: ProfessorSchema) -> Professor:
    return Professor(
        id=schema.id,
        nombres=schema.nombres,
        apellidos=schema.apellidos,
        numero_empleado=schema.numero_empleado,
        horas_clase=schema.horas_clase
    )