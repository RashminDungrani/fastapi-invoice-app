from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.core.auth import AuthHandler
from app.models.invoice_contact_model import (
    InvoiceContact,
    InvoiceContactInput,
    InvoiceContactWithInvoices,
)
from app.routes.invoice_contact.invoice_contact_dao import InvoiceContactDAO

auth_handler = AuthHandler()

router = APIRouter()


# * POST
@router.post("/create", response_model=InvoiceContact)
async def create_invoice_contact(
    inserted_invoice_contact: InvoiceContactInput,
    invoice_contact_dao: InvoiceContactDAO = Depends(),
):
    invoice_contact = await invoice_contact_dao.insert(inserted_invoice_contact=inserted_invoice_contact)
    return invoice_contact


# * GET
@router.get("/all", response_model=list[InvoiceContact])
async def get_all_invoice_contacts(
    limit: Optional[int] = Query(default=None, ge=0),
    invoice_contact_dao: InvoiceContactDAO = Depends(),
):
    invoice_contacts = await invoice_contact_dao.select_all(limit=limit)
    return invoice_contacts


@router.get("/all-with-invoices", response_model=list[InvoiceContactWithInvoices])
async def get_all_invoice_contacts_with_invoices(
    limit: Optional[int] = Query(default=None, ge=0),
    invoice_contact_dao: InvoiceContactDAO = Depends(),
):
    statement = (
        select(InvoiceContact)
        .options(
            selectinload(InvoiceContact.invoices),
        )
        .limit(limit)
    )

    result = await invoice_contact_dao.select_custom(statement)
    result = result.scalars().all()
    return result


# * PUT
@router.put("/update", response_model=InvoiceContact)
async def update_invoice_contact(
    invoice_contact_id: int,
    updated_invoice_contact: InvoiceContactInput,
    invoice_contact_dao: InvoiceContactDAO = Depends(),
):
    invoice_contact = await invoice_contact_dao.select_one(invoice_contact_id=invoice_contact_id)
    invoice_contact.modified_at = datetime.now()
    invoice_contact = await invoice_contact_dao.update(
        db_invoice_contact=invoice_contact, updated_invoice_contact=updated_invoice_contact
    )
    return invoice_contact


# * DELETE
@router.delete("/delete", status_code=204)
async def delete_invoice_contact(
    invoice_contact_id: int,
    invoice_contact_dao: InvoiceContactDAO = Depends(),
):
    invoice_contact = await invoice_contact_dao.select_one(invoice_contact_id=invoice_contact_id)
    await invoice_contact_dao.delete(invoice_contact_item=invoice_contact)
