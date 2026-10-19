from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import database

app = FastAPI(
    title = "Sales Force CRM",
    description= "A Customer Relation Management System for Business",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# database.setup_sql()

class UserCreate(BaseModel):
    name: str
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

@app.get("/customers")
def show_all(request: Request):
    result = database.show_from_sql()
    return templates.TemplateResponse(request, "customer.html", {"result": result})

# ADD CUSTOMER

@app.get("/customers/add")
def show_add_customer_form(request: Request):
    return templates.TemplateResponse(request, "add_customer.html")

@app.post("/customers/add")
def add_customer(user: UserCreate, request: Request):
    result = database.add_customer(user)
    return templates.TemplateResponse(request, "add_customer.html", {"result": result})

# DELETE CUSTOMER

@app.get("/customers/delete")
def show_delete_customer_form(request: Request):
    return templates.TemplateResponse(request, "delete_customer.html")

@app.post("/customers/delete")
def delete_customer(user: UserDelete, request: Request):
    result = database.delete_customer(user)
    return templates.TemplateResponse(request, "delete_customer.html", {"result": result})


# SEARCH CUSTOMER

@app.get("/customers/search")
def show_search_customer_form(request: Request):
    return templates.TemplateResponse(request, "search_customer.html")

@app.post("/customers/search")
def search_customers(user: UserSearch, request: Request):
    result = database.search_customer(user)
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