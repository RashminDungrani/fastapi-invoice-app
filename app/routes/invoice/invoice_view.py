from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import noload, selectinload
from sqlmodel import select

from app.core.auth import AuthHandler
from app.models.client_contact_model import ClientContact
from app.models.invoice_contact_model import InvoiceContact
from app.models.invoice_model import Invoice, InvoiceFull, InvoiceInput
from app.models.note_model import Note
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
    limit: Optional[int] = Query(default=None, ge=0),
    invoice_dao: InvoiceDAO = Depends(),
):
    invoices = await invoice_dao.select_all(limit=limit)
    return invoices


@router.get("/full", response_model=InvoiceFull)
async def get_full_invoice(
    invoice_id: int,
    invoice_dao: InvoiceDAO = Depends(),
):
    statement = (
        select(Invoice)
        .where(Invoice.id == invoice_id)
        .limit(1)
        .options(
            selectinload(Invoice.client_contact),
            selectinload(Invoice.invoice_contact),
            selectinload(Invoice.items),
            selectinload(Invoice.notes),
        )
    )

    result = await invoice_dao.select_custom(statement)
    result = result.scalar_one_or_none()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invoice id not exist")

    return InvoiceFull(**dict(result))


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
