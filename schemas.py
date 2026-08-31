from pydantic import BaseModel, Field 
from datetime import datetime 

class DocumentCreate(BaseModel):
    title: str = Field (..., min_length=3, max_length=255, description="Название документа")
    content: str = Field (..., min_length=10, description="Содержимое документа")

class DocumentResponse(BaseModel):
    id: int 
    title: str
    content: str
    summary: str | None
    status: str
    created_at: datetime
    class Config:
        from_attributes = True
