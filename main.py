from fastapi import FastAPI
from pydantic import BaseModel
import database

app = FastAPI(
    title = "Sales Force CRM",
    description= "A Customer Relation Management System for Business",
    version="1.0.0"
)

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: bool | None = None

@app.get("/")
def read_root():
    message = {"message":"Welcome to Sales Force Crm"}
    return message

