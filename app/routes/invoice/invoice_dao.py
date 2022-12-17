from fastapi import Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.dependencies import get_db_session
from app.models.invoice_model import Invoice


class InvoiceDAO:
    """Class for accessing invoice table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def select(self, invoice_id: int) -> Invoice:
        invoice = await self.session.get(Invoice, invoice_id)
        if not invoice:
            raise HTTPException(status_code=404, detail="invoice id not found")

        return invoice

    async def insert(self, inserted_invoice: Invoice) -> Invoice:
        invoice: Invoice = Invoice.from_orm(inserted_invoice)
        self.session.add(invoice)
        await self.session.commit()
        return invoice

    async def update(self, db_invoice: Invoice, updated_invoice: Invoice) -> Invoice:
        for key, value in (updated_invoice.dict(exclude_unset=True)).items():
            setattr(db_invoice, key, value)
        self.session.add(db_invoice)
        await self.session.commit()
        await self.session.refresh(db_invoice)

        return db_invoice

    async def delete(self, invoice_item: Invoice) -> None:
        await self.session.delete(invoice_item)
        await self.session.commit()
