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
from routes.central import central_router
from routes.operaciones import operations_router
from routes.brands import brands_router
from routes.expense_account import expenseAccount_router
from routes.modalities import modalities_router
from routes.extras import extras_router
from routes.reports.partsrelationship import partsrelationshipReports_router
from routes.reports.relationshiprevenues import relationshiprevenuesReports_router
from routes.reports.pandgstatus import pandgstatus_router
from routes.company import company_router
from routes.collection_account import collectionAccount_router
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
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
app.include_router(central_router)
app.include_router(operations_router)
app.include_router(brands_router)
app.include_router(expenseAccount_router)
app.include_router(modalities_router)
app.include_router(extras_router)
app.include_router(partsrelationshipReports_router)
app.include_router(relationshiprevenuesReports_router)
app.include_router(pandgstatus_router)
app.include_router(company_router)
app.include_router(collectionAccount_router)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/")
def main():
  return {"Hello": "World"}
