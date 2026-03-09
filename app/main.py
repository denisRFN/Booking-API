from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.session import Base, engine
from app.routers import auth, users, desks, reservations, availability


def create_app() -> FastAPI:
    Base.metadata.create_all(bind=engine)

    app = FastAPI(title="Booking API", version="1.0.0")

    origins: list[str] = []
    if settings.BACKEND_CORS_ORIGINS:
        origins = [o.strip() for o in settings.BACKEND_CORS_ORIGINS.split(",") if o.strip()]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(desks.router)
    app.include_router(reservations.router)
    app.include_router(availability.router)

    return app


app = create_app()

