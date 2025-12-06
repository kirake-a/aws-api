from datetime import datetime
from passlib.context import CryptContext
import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Recibe una contraseña en texto plano y devuelve el hash encriptado.
    Ejemplo: 'p4ssw0rd' -> '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWrnMnz...'
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si la contraseña en texto plano coincide con el hash guardado.
    IMPORTANTE: Bcrypt usa 'salts' aleatorios, por lo que el hash siempre cambia.
    No puedes simplemente hashear y comparar strings, debes usar esta función.
    """
    return pwd_context.verify(plain_password, hashed_password)

def generate_session_string() -> str:
    """
    Genera un string aleatorio seguro de 128 caracteres hexadecimales.
    secrets.token_hex(64) genera 64 bytes = 128 caracteres hex.
    """
    return secrets.token_hex(64)

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