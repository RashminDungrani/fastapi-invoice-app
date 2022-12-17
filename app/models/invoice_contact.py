"""
TODO: Write about this model
"""
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.invoice_model import Invoice


class InvoiceContact(SQLModel, table=True):
    __tablename__: str = "invoice_contact"

    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    name: str = Field(index=True, min_length=2)
    mobile: str = Field(index=True, min_length=7)

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)

    invoices: list["Invoice"] = Relationship(back_populates="invoice_contact")  # parent
