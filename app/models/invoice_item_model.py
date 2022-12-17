import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Column, Enum, Field, Relationship

from app.db.base import SQLModel

if TYPE_CHECKING:
    from app.models.invoice_model import Invoice


class InvoiceItem(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    invoice_id: int = Field(foreign_key="Invoice.id")
    name: str = Field(index=True, min_length=2, max_length=40)
    price: float = Field(nullable=False)
    quantity: Optional[int] = Field(default=1, nullable=False)
    desc: Optional[str] = Field(default=None, nullable=True)

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)

    invoice: Optional["Invoice"] = Relationship(back_populates="items")
