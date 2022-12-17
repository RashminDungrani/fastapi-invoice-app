from typing import Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import selectinload
from sqlmodel import delete, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.dependencies import get_db_session
from app.models.invoice_item_model import InvoiceItem, InvoiceItemInput


class InvoiceItemDAO:
    """Class for accessing InvoiceItem table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def select_one(self, invoice_item_id: int) -> InvoiceItem:
        invoice_item = await self.session.get(InvoiceItem, invoice_item_id)
        if not invoice_item:
            raise HTTPException(status_code=404, detail="invoice_item id not found")

        return invoice_item

    async def select_all(self, offset: Optional[int] = None, limit: Optional[int] = None) -> list[InvoiceItem]:
        query = select(InvoiceItem).offset(offset).limit(limit)
        invoice_items = (await self.session.execute(query)).scalars().all()
        return invoice_items

    async def insert(self, inserted_invoice_item: InvoiceItemInput) -> InvoiceItem:
        try:
            invoice_item: InvoiceItem = InvoiceItem.from_orm(inserted_invoice_item)
            self.session.add(invoice_item)
            await self.session.commit()
            return invoice_item
        except exc.IntegrityError as error:
            print(error.code, error.params)
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Invoice id {inserted_invoice_item.invoice_id} does not exist",
            )

    async def update(self, db_invoice_item: InvoiceItem, updated_invoice_item: InvoiceItemInput) -> InvoiceItem:

        for key, value in (updated_invoice_item.dict(exclude_unset=True)).items():
            setattr(db_invoice_item, key, value)
        self.session.add(db_invoice_item)
        await self.session.commit()
        await self.session.refresh(db_invoice_item)

        return db_invoice_item

    async def delete(self, invoice_item_item: InvoiceItem) -> None:
        await self.session.delete(invoice_item_item)
        await self.session.commit()
