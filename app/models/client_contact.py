"""
TODO: Write about this model
"""
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.db.base import SQLModel

if TYPE_CHECKING:
    from app.models.invoice_model import Invoice


class ClientContact(SQLModel, table=True):

    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    client_name: str = Field(index=True, min_length=2)
    client_phone: str = Field(index=True, min_length=7)

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)

    invoices: list["Invoice"] = Relationship(back_populates="client_contact")  # parent
