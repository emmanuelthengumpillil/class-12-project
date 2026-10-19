from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
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
def add_customer(request: Request,
                 name:str = Form(...),
                 phone: str = Form(...),
                 email: str = Form(...)):
    values = {"name": name, "phone": phone, "email": email}
    result = database.add_customer(values)
    return RedirectResponse(url="/customers", status_code=303)


# DELETE CUSTOMER
@app.post("/customers/delete/{id}")
def delete_customer(id: int, request: Request):
    database.delete_customer(id)
    return RedirectResponse(url="/customers", status_code=303)


# EDIT CUSTOMER
@app.get("/customers/edit/{id}")
def show_edit_customer_form(request: Request, id:int):
    values = {'id': id}
    values = database.search_customers_by_id(values)
    return templates.TemplateResponse(request, "edit_customers.html", {'values': values[0]})

@app.post("/customers/edit/{id}")
def edit_customer(request: Request, id: int,
                  name: str = Form('...'),
                  phone: str = Form('...'),
                  email: str = Form('...')):
    values = {'id': id, 'name': name, 'phone': phone, 'email': email}
    database.edit_customer(values)
    return RedirectResponse(url="/customers", status_code=303)

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