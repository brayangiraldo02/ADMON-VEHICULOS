from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.dbconnection import Base, engine
from routes.reports import reports_router
from fastapi.staticfiles import StaticFiles
from routes.users import users_router

app = FastAPI()

origins = [
  "http://localhost",
  "http://localhost:4200",
  "http://localhost:4200/login/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(reports_router)
app.include_router(users_router)
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/")
def main():
  return {"Hello": "World"}

