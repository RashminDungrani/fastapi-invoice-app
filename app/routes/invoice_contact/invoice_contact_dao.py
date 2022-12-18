from typing import Any, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import Executable
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.dependencies import get_db_session
from app.models.invoice_contact_model import InvoiceContact, InvoiceContactInput


class InvoiceContactDAO:
    """Class for accessing InvoiceContact table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def select_one(self, invoice_contact_id: int) -> InvoiceContact:
        invoice_contact = await self.session.get(InvoiceContact, invoice_contact_id)
        if not invoice_contact:
            raise HTTPException(status_code=404, detail="invoice_contact id not found")

        return invoice_contact

    async def select_all(self, offset: Optional[int] = None, limit: Optional[int] = None) -> list[InvoiceContact]:
        query = select(InvoiceContact).offset(offset).limit(limit)
        invoice_contacts = (await self.session.execute(query)).scalars().all()
        return invoice_contacts

    async def select_custom(self, statement: Executable) -> Any:
        return await self.session.execute(statement)

    async def insert(self, inserted_invoice_contact: InvoiceContactInput) -> InvoiceContact:
        invoice_contact: InvoiceContact = InvoiceContact.from_orm(inserted_invoice_contact)
        self.session.add(invoice_contact)
        await self.session.commit()
        return invoice_contact

    async def update(
        self, db_invoice_contact: InvoiceContact, updated_invoice_contact: InvoiceContactInput
    ) -> InvoiceContact:

        for key, value in (updated_invoice_contact.dict(exclude_unset=True)).items():
            setattr(db_invoice_contact, key, value)
        self.session.add(db_invoice_contact)
        await self.session.commit()
        await self.session.refresh(db_invoice_contact)

        return db_invoice_contact

    async def delete(self, invoice_contact_item: InvoiceContact) -> None:
        await self.session.delete(invoice_contact_item)
        await self.session.commit()
