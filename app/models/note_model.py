"""
Note model for perticular invoice note
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.invoice_model import Invoice


class NoteInput(SQLModel):
    note: str = Field(index=True, min_length=1)
    invoice_id: int = Field(foreign_key="Invoice.id")


class Note(NoteInput, table=True):
    __tablename__: str = "Note"
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)

    invoice: Optional["Invoice"] = Relationship(back_populates="notes")  # child


class NoteWithInvoice(NoteInput):
    id: int
    created_at: datetime
    modified_at: datetime
    deleted_at: Optional[datetime]
    invoice: Optional["Invoice"]
