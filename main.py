from fastapi import FastAPI
from pydantic import BaseModel, Field
import database

app = FastAPI(
    title = "Sales Force CRM",
    description= "A Customer Relation Management System for Business",
    version="1.0.0"
)
database.setup_sql()

class UserCreate(BaseModel):
    name: str = Field(min_length=2)
    phone: str = Field(min_length=10, max_length=12)
    email:str

class UserDelete(BaseModel):
    name: str
    phone: str =  Field(min_length=10, max_length=12)
    email: str

class UserSearch(BaseModel):
    name : str

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


@app.post("/users/search")
def search_user(user: UserSearch):
    result = database.search_user(user)
    return result


@app.get("/showtables")
def show_tables(limit: int = None):
    result = list(database.show_tables())
    if limit:
        result = list(database.show_tables())[:limit]
        return result
    return result

@app.get("/desc{tablename}")
def desc_table(tablename):
    result = database.desc_table(tablename)
    return result