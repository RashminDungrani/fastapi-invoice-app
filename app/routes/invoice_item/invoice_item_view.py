from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.auth import AuthHandler
from app.models.invoice_item_model import InvoiceItem, InvoiceItemInput
from app.routes.invoice_item.invoice_item_dao import InvoiceItemDAO

auth_handler = AuthHandler()

router = APIRouter()


# * POST
@router.post("/create", response_model=InvoiceItem)
async def create_invoice_item(
    inserted_invoice_item: InvoiceItemInput,
    invoice_item_dao: InvoiceItemDAO = Depends(),
):
    invoice_item = await invoice_item_dao.insert(inserted_invoice_item=inserted_invoice_item)
    return invoice_item


# * GET
@router.get("/all", response_model=list[InvoiceItem])
async def get_all_invoice_items(
    limit: Optional[int] = Query(default=None, ge=0),
    invoice_item_dao: InvoiceItemDAO = Depends(),
):
    invoice_items = await invoice_item_dao.select_all(limit=limit)
    return invoice_items


# * PUT
@router.put("/update", response_model=InvoiceItem)
async def update_invoice_item(
    invoice_item_id: int,
    updated_invoice_item: InvoiceItemInput,
    invoice_item_dao: InvoiceItemDAO = Depends(),
):
    invoice_item = await invoice_item_dao.select_one(invoice_item_id=invoice_item_id)
    invoice_item.modified_at = datetime.now()
    invoice_item = await invoice_item_dao.update(
        db_invoice_item=invoice_item, updated_invoice_item=updated_invoice_item
    )
    return invoice_item


# * DELETE
@router.delete("/delete", status_code=204)
async def delete_invoice_item(
    invoice_item_id: int,
    invoice_item_dao: InvoiceItemDAO = Depends(),
):
    invoice_item = await invoice_item_dao.select_one(invoice_item_id=invoice_item_id)
    await invoice_item_dao.delete(invoice_item_item=invoice_item)
