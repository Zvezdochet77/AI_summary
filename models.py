from sqlalchemy import String, Text, DateTime 
from sqlalchemy.orm import Mapped, mapped_column 
from datetime import datetime, timezone 
from database import Base 

class Document (Base):
    __tablename__ = "documents"

    id: Mapped [int] = mapped_column (primary_key=True, index=True)
    title: Mapped [str] = mapped_column (String (255), index=True, nullable=False)
    content: Mapped [str] = mapped_column (Text, nullable=False)
    summary: Mapped [str | None] = mapped_column (Text, nullable=True)
    status: Mapped [str] = mapped_column (String (50), default="pending")
    created_at: Mapped [datetime] = mapped_column (DateTime(timezone=True), default=datetime.now(timezone.utc)) 
    