from fastapi import FastAPI
from app.api import reservations

app = FastAPI()

app.include_router(reservations.router)
