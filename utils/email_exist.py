from typing import Any

def email_exists(email: str, items: list[Any]) -> bool:
    for item in items:
        if item.email == email:
            return True
    return False