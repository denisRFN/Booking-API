from fastapi import FastAPI

from app.db.database import Base, engine

# IMPORTANT – importăm toate modelele
from app.models import user
from app.models import desk

from app.api import reservations
from app.api import desks
from app.api import auth
from app.api import users


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(desks.router)
app.include_router(reservations.router)
app.include_router(auth.router)
app.include_router(users.router)