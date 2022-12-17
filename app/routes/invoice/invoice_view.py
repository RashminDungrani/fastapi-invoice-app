from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.auth import AuthHandler
from app.models.invoice_model import Invoice
from app.paths import paths
from app.routes.invoice.invoice_dao import InvoiceDAO

auth_handler = AuthHandler()

router = APIRouter()


# * GET
@router.get("/all", response_model=list[Invoice])
async def get_all_invoices(
    limit: Optional[int] = Query(default=100, ge=0),
    invoice_dao: InvoiceDAO = Depends(),
):
    invoices = await invoice_dao.select_all(offset=0, limit=limit)
    return invoices


# * GET

# * POST
