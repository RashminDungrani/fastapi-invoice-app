from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.auth import AuthHandler
from app.models.invoice_model import Invoice, InvoiceInput
from app.routes.invoice.invoice_dao import InvoiceDAO

auth_handler = AuthHandler()

router = APIRouter()


# * POST
@router.post("/create", response_model=Invoice)
async def create_invoice(
    inserted_invoice: InvoiceInput,
    invoice_dao: InvoiceDAO = Depends(),
):
    invoice = await invoice_dao.insert(inserted_invoice=inserted_invoice)
    return invoice


# * GET
@router.get("/all", response_model=list[Invoice])
async def get_all_invoices(
    limit: Optional[int] = Query(default=100, ge=0),
    invoice_dao: InvoiceDAO = Depends(),
):
    invoices = await invoice_dao.select_all(limit=limit)
    return invoices


# * PUT
@router.put("/update", response_model=Invoice)
async def update_invoice(
    invoice_id: int,
    updated_invoice: InvoiceInput,
    invoice_dao: InvoiceDAO = Depends(),
):
    invoice = await invoice_dao.select_one(invoice_id=invoice_id)
    invoice.modified_at = datetime.now()
    invoice = await invoice_dao.update(db_invoice=invoice, updated_invoice=updated_invoice)
    return invoice


# * DELETE
@router.delete("/delete", status_code=204)
async def delete_invoice(
    invoice_id: int,
    invoice_dao: InvoiceDAO = Depends(),
):
    invoice = await invoice_dao.select_one(invoice_id=invoice_id)
    await invoice_dao.delete(invoice_item=invoice)
