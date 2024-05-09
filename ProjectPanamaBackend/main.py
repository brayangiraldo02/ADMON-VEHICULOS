from fastapi import FastAPI
from config.dbconnection import Base, engine
from routes.reports import reports_router
from fastapi.staticfiles import StaticFiles
from routes.users import users_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(reports_router)
app.include_router(users_router)
app.mount("/static", StaticFiles(directory="static", html=True), name ="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/")
def main():
  return {"Hello": "World"}

