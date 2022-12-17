"""
TODO: Write about this model
"""
import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Column, Enum, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.invoice_model import Invoice

# class EnumClass(str, enum.Enum):
#     VAL = "VAL"


class Note(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    note: str = Field(index=True, min_length=1)
    invoice_id: int = Field(foreign_key="invoice.id")

    invoice: Optional["Invoice"] = Relationship(back_populates="notes")  # child

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)
