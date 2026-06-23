from pydantic import BaseModel
from typing import Optional


class ValidationWarning(BaseModel):
    field: str
    severity: str
    message: str
    suggestion: Optional[str] = None