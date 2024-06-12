from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.dbconnection import Base, engine
from routes.reports import reports_router
from fastapi.staticfiles import StaticFiles
from routes.users import users_router
from routes.owners import owners_router
from routes.states import states_router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://admon-vehiculos.vercel.app", "http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(reports_router)
app.include_router(users_router)
app.include_router(owners_router)
app.include_router(states_router)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/")
def main():
  return {"Hello": "World"}

