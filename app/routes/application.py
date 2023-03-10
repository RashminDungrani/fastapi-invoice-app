from os.path import join

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, UJSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.settings import settings
from app.db.lifetime import register_shutdown_event, register_startup_event
from app.paths import paths
from app.routes.router import api_router


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """

    app = FastAPI(
        title=f"{settings.app_name} - Swagger UI",
        description=settings.app_desc,
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    # origins = [
    #     "http://192.168.1.237",
    #     "http://192.168.1.237:8000",
    # ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Add Icon
    @app.get("/favicon.ico", include_in_schema=False)
    async def _() -> FileResponse:
        return FileResponse(join(paths.static, "favicon.ico"))

    # Main router for the API.
    app.include_router(router=api_router)

    # mount static posts
    app.mount("/static", StaticFiles(directory=paths.static), name="static")

    return app
