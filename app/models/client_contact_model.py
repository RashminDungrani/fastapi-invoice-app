"""
Client contact for invoice
One client contact can have multiple invoices
"""

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.invoice_model import Invoice


class ClientContactInput(SQLModel):
    client_name: str = Field(index=True, min_length=2)
    client_phone: str = Field(index=True, min_length=7)


class ClientContactBase(ClientContactInput):
    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)


class ClientContact(ClientContactBase, table=True):
    __tablename__: str = "ClientContact"
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)

    invoices: list["Invoice"] = Relationship(back_populates="client_contact")  # parent


class ClientContactWithInvoices(ClientContactBase):
    id: int
    invoices: list["Invoice"]
