from datetime import datetime
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field
from fastapi import status

T = TypeVar('T')

class ResponseWrapper(BaseModel, Generic[T]):
    success: bool
    message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now().isoformat())
    status_code: int = status.HTTP_200_OK
    data: Optional[T] = None