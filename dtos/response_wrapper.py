from datetime import datetime
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')

class ResponseWrapper(BaseModel, Generic[T]):
    success: bool
    message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now().isoformat())
    data: Optional[T] = None