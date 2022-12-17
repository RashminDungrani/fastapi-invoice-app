"""
TODO: Write about this model
"""
import enum
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Column, Enum, Field, ForeignKey, Relationship, SQLModel

if TYPE_CHECKING:

    from app.models.invoice_item_model import InvoiceItem
    from app.models.note_model import Note


class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    total_price: float = Field(nullable=False)

    client_contact_id: int = Field(foreign_key="client_contact.id")

    invoice_contact_id: int = Field(foreign_key="invoice_contact.id")

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)

    items: list["InvoiceItem"] = Relationship(back_populates="invoice")  # parent
    notes: list["Note"] = Relationship(back_populates="invoice")  # parent
    invoice_contact: Optional["Invoice"] = Relationship(back_populates="invoices")  # child
    client_contact: Optional["Invoice"] = Relationship(back_populates="invoices")  # child
