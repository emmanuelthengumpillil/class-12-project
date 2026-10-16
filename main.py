from fastapi import FastAPI
from pydantic import BaseModel
import database

app = FastAPI(
    title = "Sales Force CRM",
    description= "A Customer Relation Management System for Business",
    version="1.0.0"
)

class UserCreate(BaseModel):
    id: int
    name: str
    phone: str
    email:str

class UserDelete(BaseModel):
    name: str
    phone: str
    email: str

@app.get("/")
def read_root():
    message = {"message":"Welcome to Sales Force Crm"}
    return message

@app.get("/users")
def show_all():
    table = "customer"
    result = database.show_from_sql(table)
    return result

@app.post("/users/add")
def add_user(user: UserCreate):
    result = database.add_user(user)
    return result

@app.post("/users/delete")
def delete_user(user: UserDelete):
    result = database.delete_user(user)
    return result
