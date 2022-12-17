"""
TODO: Write about this model
"""
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.db.base import SQLModel

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
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)

    invoices: list["Invoice"] = Relationship(back_populates="client_contact")  # parent