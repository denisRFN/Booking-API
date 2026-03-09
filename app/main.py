from fastapi import FastAPI
from app.api import reservations
from app.api import desks

app = FastAPI()

app.include_router(desks.router)
app.include_router(reservations.router)
