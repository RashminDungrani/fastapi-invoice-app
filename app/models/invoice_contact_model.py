"""
Invoice contact for invoice
One invoice contact can have multiple invoices
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.invoice_model import Invoice


class InvoiceContactInput(SQLModel):
    name: str = Field(index=True, min_length=2)
    mobile: str = Field(index=True, min_length=7)


class InvoiceContact(InvoiceContactInput, table=True):
    __tablename__: str = "InvoiceContact"

    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)

    invoices: list["Invoice"] = Relationship(
        back_populates="invoice_contact",
        sa_relationship_kwargs=dict(primaryjoin="InvoiceContact.id == Invoice.invoice_contact_id"),
    )  # parent


class InvoiceContactWithInvoices(InvoiceContactInput):
    id: int
    created_at: datetime
    modified_at: datetime
    deleted_at: Optional[datetime]
    invoices: list["Invoice"]
