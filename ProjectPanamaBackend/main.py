from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.dbconnection import Base, engine
from fastapi.staticfiles import StaticFiles
from routes.users import users_router
from routes.owners import owners_router
from routes.states import states_router
from dotenv import load_dotenv
from routes.reports.feespaid import feespaidReports_router
from routes.reports.owners import ownersReports_router
from routes.reports.statevehiclefleet import statevehiclefleetReports_router
from routes.drivers import drivers_router
from routes.vehicles import vehicles_router
from routes.cities import cities_router
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

app.include_router(feespaidReports_router)
app.include_router(ownersReports_router)
app.include_router(statevehiclefleetReports_router)
app.include_router(users_router)
app.include_router(owners_router)
app.include_router(states_router)
app.include_router(drivers_router)
app.include_router(vehicles_router)
app.include_router(cities_router)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/")
def main():
  return {"Hello": "World"}
