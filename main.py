from fastapi import FastAPI, Request,Form, Cookie, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field
import database
import secrets
import graph


app = FastAPI(
    title = "Zerohour CRM",
    description= "A Customer Relation Management System for Business",
    version="1.0.0"
)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# GLobal variables
templates.env.globals['username'] = 'Emmanuel'
templates.env.globals['app_name'] = 'Zero Hour'

database.setup_tables()

# GETTING COOKIES
def get_current_user(session_token: str | None = Cookie(default=None)):
    if session_token is None:
        raise HTTPException(
            status_code = 401,
            detail = "Not - authenticated please log in")
    return session_token

@app.get("/")
def landing_page(request: Request):
    return templates.TemplateResponse(request, "landing.html")

@app.get("/home")
def home(request: Request, current_user: str = Depends(get_current_user)):
    chart_url = graph.usercount_analysis()
    no_of_customers = database.no_of_users()[0]['count']
    return templates.TemplateResponse(request, "home.html", {'chart_url': chart_url, 'result': no_of_customers})

# SELECT
@app.get("/customers")
def show_all(request: Request, current_user: str = Depends(get_current_user)):
    result = database.show_from_sql()
    return templates.TemplateResponse(request, "customer.html", {"result": result})


# ADD CUSTOMER
@app.get("/customers/add")
def show_add_customer_form(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse(request, "add_customer.html")

@app.post("/customers/add")
def add_customer(request: Request,
                 name:str = Form(...),
                 phone: str = Form(...),
                 email: str = Form(...),
                 current_user: str = Depends(get_current_user)):
    values = {"name": name, "phone": phone, "email": email, 'table':'customers'}
    result = database.add_customer(values)
    return RedirectResponse(url="/customers", status_code=303)


# DELETE CUSTOMER
@app.post("/customers/delete/{id}")
def delete_customer(id: int, request: Request, current_user: str = Depends(get_current_user)):
    database.delete_customer(id)
    return RedirectResponse(url="/customers", status_code=303)


# EDIT CUSTOMER
@app.get("/customers/edit/{id}")
def show_edit_customer_form(request: Request, id:int, current_user: str = Depends(get_current_user)):
    values = {'id': id, 'table': 'customers'}
    values = database.search_customers_by_id(values)
    return templates.TemplateResponse(request, "edit_customers.html", {'values': values[0]})

@app.post("/customers/edit/{id}")
def edit_customer(request: Request, id: int,
                  name: str = Form('...'),
                  phone: str = Form('...'),
                  email: str = Form('...'),
                  current_user: str = Depends(get_current_user),):
    values = {'id': id, 'name': name, 'phone': phone, 'email': email, 'table': 'customers'}
    database.edit_customer(values)
    return RedirectResponse(url="/customers", status_code=303)


# SEARCH CUSTOMER
@app.get("/customers/search")
def show_search_customer_form(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse(request, "search_customer.html")

@app.post("/customers/search")
def search_customers(name: str, request: Request, current_user: str = Depends(get_current_user)):
    result = database.search_customer(user)
    return templates.TemplateResponse(request, "search_customer.html", {"result": result})


# SIGN IN 
@app.get("/signin")
def show_signin_form(request: Request, message: str = None):
    return templates.TemplateResponse(request, "signin.html", {'message': message})

@app.post("/signin")
def signin(email: str = Form(...),
           password: str = Form(...)):
    values = {"email": email, "password": password, 'table': 'users'}
    is_signedin = database.signin_customer(values)
    print(is_signedin)
    if not is_signedin['status']:
        if is_signedin['message'] == 'password_error':
            return RedirectResponse(url="/signin?message=Incorrect+Password", status_code=303)
        else:
            return RedirectResponse(url="/signin?message=User+not+found", status_code=303)

    response = RedirectResponse(url="/?message=Signin+successfull", status_code=303)

    session_token = secrets.token_hex(100)
    response.set_cookie(
        key = "session_token",
        value = session_token,
        httponly = True,
        secure = False,
        max_age = 3600)

    return response

    
# SIGNUP
@app.get('/signup')
def show_signup_form(request: Request, message: str = None):
    return templates.TemplateResponse(request, 'signup.html', {'message': message})

@app.post('/signup')
def signup(name: str = Form(...),
           email: str = Form(...),
           phone: str = Form(...),
           company_name: str = Form(...),
           password: str = Form(...)):
    values = {'name': name, 'email':email, 'phone': phone, 'company_name': company_name, 'password': password, 'table': 'users'}
    status = database.signup_customer(values)
    if status:
        return RedirectResponse(url="/signin?message=Signup+successful.+Please+sign+in.", status_code=303)
    else:
        return RedirectResponse(url="/signup?message=User+already+exists", status_code=303)


@app.get("/showtables")
def show_tables(limit: int = None, request = Request, current_user: str = Depends(get_current_user)):
    result = list(database.show_tables())
    if limit:
        result = list(database.show_tables())[:limit]
        return templates.TemplateResponse(request, "show_tables.html", {"result": result, "limit": limit})
    return templates.TemplateResponse(request, "show_tables.html", {"result": result, "limit": None})

@app.get("/desc{tablename: str}")
def desc_table(tablename):
    result = database.desc_table(tablename)
    return result


@app.get("/logout")
def logout(current_user: str = Depends(get_current_user)):
    response = RedirectResponse(url="/signin?message=Logged+out+successfully", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="session_token")
    return response