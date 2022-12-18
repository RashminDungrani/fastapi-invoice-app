"""
app/models/__init__.py

from https://github.com/tiangolo/sqlmodel/issues/121#issuecomment-935656778
Import the various model modules in one place and resolve forward refs.
"""


# AccountOutputWithCustomer.update_forward_refs(CustomerOutput=CustomerOutput)
# CustomerOutputWithAccounts.update_forward_refs(AccountOutput=AccountOutput)

# from app.models.invoice_model import Invoice

# Invoice.update_forward_refs()

import pkgutil
from pathlib import Path

from app.models.client_contact_model import ClientContact, ClientContactWithInvoices
from app.models.invoice_contact_model import InvoiceContact, InvoiceContactWithInvoices
from app.models.invoice_item_model import InvoiceItem
from app.models.invoice_model import Invoice, InvoiceFull
from app.models.note_model import Note, NoteWithInvoice

InvoiceFull.update_forward_refs(
    ClientContact=ClientContact, InvoiceContact=InvoiceContact, InvoiceItem=InvoiceItem, Note=Note
)

InvoiceContactWithInvoices.update_forward_refs(Invoice=Invoice)
ClientContactWithInvoices.update_forward_refs(Invoice=Invoice)
NoteWithInvoice.update_forward_refs(Invoice=Invoice)


def load_all_models() -> None:
    """Load all models from this folder."""
    package_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(package_dir)],
        prefix="app.models.",
    )
    for module in modules:
        print(module.name)
        __import__(module.name)  # noqa: WPS421
