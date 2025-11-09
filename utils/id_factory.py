from datetime import datetime


def generate_id() -> str:
    import uuid
    return str(uuid.uuid4())

def _create_id_postfix() -> str:
    import random
    first_two_year_digits = datetime.now().year % 100
    cero = "00"
    last_four_digits = str(random.randint(0, 9999)).zfill(4)

    return f"{first_two_year_digits}{cero}{last_four_digits}"

def generate_registration() -> str:
    return f"A{_create_id_postfix()}"

def generate_employee_number() -> str:
    return f"E{_create_id_postfix()}"