from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import database

app = FastAPI(
    title = "Sales Force CRM",
    description= "A Customer Relation Management System for Business",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

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
def read_root(request: Request):
    message = {"message":"Welcome to Sales Force Crm"}
    return templates.TemplateResponse(request, "home.html", {"posts": message})

@app.get("/users")
def show_all(request: Request):
    table = "customer"
    result = database.show_from_sql(table)
    return templates.TemplateResponse(request, "customer.html", {"result": result})

@app.post("/users/add")
def add_user(user: UserCreate, request: Request):
    result = database.add_user(user)
    return templates.TemplateResponse(request, "add_customer.html", {"result": result})

@app.post("/users/delete")
def delete_user(user: UserDelete, request: Request):
    result = database.delete_user(user)
    return templates.TemplateResponse(request, "delete_customer.html", {"result": result})


@app.post("/users/search")
def search_user(user: UserSearch, request: Request):
    result = database.search_user(user)
    return templates.TemplateResponse(request, "search_customer.html", {"result": result})


@app.get("/showtables")
def show_tables(limit: int = None, request = Request):
    result = list(database.show_tables())
    if limit:
        result = list(database.show_tables())[:limit]
        return templates.TemplateResponse(request, "show_tables.html", {"result": result, "limit": limit})
    return templates.TemplateResponse(request, "show_tables.html", {"result": result, "limit": None})

@app.get("/desc{tablename: str}")
def desc_table(tablename):
    result = database.desc_table(tablename)
    return result