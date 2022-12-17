"""
TODO: Write about this model
"""
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.db.base import SQLModel

if TYPE_CHECKING:
    from app.models.client_contact import ClientContact
    from app.models.invoice_contact import InvoiceContact
    from app.models.invoice_item_model import InvoiceItem
    from app.models.note_model import Note


class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None, nullable=False)
    total_price: float = Field(nullable=False)

    created_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    modified_at: Optional[datetime] = Field(default=datetime.now(), nullable=False)
    deleted_at: Optional[datetime] = Field(nullable=True)

    invoice_contact_id: int = Field(foreign_key="InvoiceContact.id")  # fk
    client_contact_id: int = Field(foreign_key="ClientContact.id")  # fk

    invoice_contact: Optional["InvoiceContact"] = Relationship(
        back_populates="invoices",
    )  # child

    client_contact: Optional["ClientContact"] = Relationship(back_populates="invoices")  # child

    items: list["InvoiceItem"] = Relationship(
        back_populates="invoice",
        # sa_relationship_kwargs=dict(
        # primaryjoin="Invoice.id==InvoiceItem.id",
        # lazy="noload",
        #     viewonly=True,
        # ),
    )  # parent
    notes: list["Note"] = Relationship(back_populates="invoice")  # parent
