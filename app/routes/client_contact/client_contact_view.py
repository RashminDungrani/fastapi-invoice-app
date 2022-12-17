from typing import Optional

from fastapi import APIRouter, Depends, status

from app.core.auth import AuthHandler
from app.models.client_contact_model import ClientContact
from app.routes.client_contact.client_contact_dao import ClientContactDAO
from app.routes.invoice.invoice_dao import InvoiceDAO

auth_handler = AuthHandler()

router = APIRouter()


# * GET
@router.get("/all", response_model=list[ClientContact])
async def get_all_invoices(
    client_contact_dao: ClientContactDAO = Depends(),
):
    clientContacts = await client_contact_dao.select_all()
    return clientContacts


# * GET

# * POST
