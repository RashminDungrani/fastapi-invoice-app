from fastapi.routing import APIRouter

from app.routes.token import token_router

api_router = APIRouter(prefix="/api")
api_router.include_router(token_router, tags=["Token"], include_in_schema=False)

# api_router.include_router(
#     super_admin.router, prefix="/super-admin", tags=["Super Admin"]
# )

