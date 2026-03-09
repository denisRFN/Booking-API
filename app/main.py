from fastapi import FastAPI
from app.api import reservations
from app.api import desks
from app.models.desk import Base
from app.db.database import engine
from app.api import auth
from app.api import users


app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(desks.router)
app.include_router(reservations.router)
app.include_router(auth.router)
app.include_router(users.router)
