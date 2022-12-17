from fastapi.routing import APIRouter

from app.routes import (
    client_contact,
    invoice,
    invoice_contact,
    invoice_item,
    note,
    super_admin,
)
from app.routes.token import token_router

api_router = APIRouter(prefix="/api")
api_router.include_router(token_router, tags=["Token"], include_in_schema=False)

api_router.include_router(super_admin.router, prefix="/super-admin", tags=["Super Admin"])
api_router.include_router(invoice.router, prefix="/invoice", tags=["Invoice"])
api_router.include_router(client_contact.router, prefix="/client-contact", tags=["Client Contact"])
api_router.include_router(invoice_contact.router, prefix="/invoice-contact", tags=["Invoice Contact"])
api_router.include_router(invoice_item.router, prefix="/invoice-item", tags=["Invoice Item"])
api_router.include_router(note.router, prefix="/note", tags=["Note"])
