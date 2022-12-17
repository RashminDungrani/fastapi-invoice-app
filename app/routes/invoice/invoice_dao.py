from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import noload, selectinload
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.dependencies import get_db_session
from app.models.invoice_model import Invoice, InvoiceInput


class InvoiceDAO:
    """Class for accessing invoice table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def select_one(self, invoice_id: int) -> Invoice:
        invoice = await self.session.get(Invoice, invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="invoice id not found")

        return invoice

    async def select_all(self, offset: Optional[int] = None, limit: Optional[int] = None) -> list[Invoice]:
        query = select(Invoice).offset(offset).limit(limit)

        invoices = (await self.session.execute(query)).scalars().all()
        return invoices

    async def insert(self, inserted_invoice: InvoiceInput) -> Invoice:
        try:
            invoice: Invoice = Invoice.from_orm(inserted_invoice)
            self.session.add(invoice)
            await self.session.commit()
            print("after commit")
            return invoice
        except exc.IntegrityError as error:
            print(error.code, error.params)
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Client contact id {inserted_invoice.client_contact_id} or/and Invoice contact id {inserted_invoice.invoice_contact_id} not exist",
            )

    async def update(self, db_invoice: Invoice, updated_invoice: InvoiceInput) -> Invoice:
        for key, value in (updated_invoice.dict(exclude_unset=True)).items():
            setattr(db_invoice, key, value)
        self.session.add(db_invoice)
        await self.session.commit()
        await self.session.refresh(db_invoice)

        return db_invoice

    async def delete(self, invoice_item: Invoice) -> None:
        # TODO: use this if this works
        # delete(invoice_item)
        await self.session.delete(invoice_item)
        await self.session.commit()
