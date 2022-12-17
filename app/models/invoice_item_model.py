"""
invoice Item model for each invoice items
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Column, Enum, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.invoice_model import Invoice


class InvoiceItemInput(SQLModel):
    invoice_id: int = Field(foreign_key="Invoice.id")
    name: str = Field(index=True, min_length=2, max_length=40)
    price: float = Field(nullable=False)
    quantity: Optional[int] = Field(default=1, nullable=False)
    desc: Optional[str] = Field(default=None, nullable=True)


class InvoiceItem(InvoiceItemInput, table=True):
    __tablename__: str = "InvoiceItem"
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)

    invoice: Optional["Invoice"] = Relationship(
        back_populates="items", sa_relationship_kwargs=dict(primaryjoin="InvoiceItem.invoice_id==Invoice.id")
    )
