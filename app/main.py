import json
import pathlib

from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.users.models import User
from . import config, db
from .users.schemas import UserSignupSchema, UserLoginSchema

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"

app = FastAPI()
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

DB_SESSION = None
settings = config.get_settings()


@app.on_event("startup")
def on_startup():
    print("Hello World")
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("home.html", context)


@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("auth/login.html", context)


@app.post("/login")
def login_post_view(
        request: Request,
        email: str = Form(...),
        password: str = Form(...)
):
    cleaned_data = UserLoginSchema(
        email=email,
        password=password
    )
    return templates.TemplateResponse("auth/login.html")


@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    context = {
        "request": request
    }
    return templates.TemplateResponse("auth/signup.html", context)


@app.post("/signup")
def signup_post_view(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        password_confirm: str = Form(...)
):
    data = {}
    errors = []
    error_str = ""
    context = {
        "request": request,
        "data": data,
        "errors": errors,
    }

    try:
        cleaned_data = UserSignupSchema(
            email=email,
            password=password,
            password_confirm=password_confirm
        )
        data = cleaned_data.dict()
    except ValidationError as e:
        error_str = e.json()

    try:
        errors = json.loads(error_str)
    except Exception as e:
        errors = [{"loc": "non_field_error", "msg": "Unknown"}]

    print(cleaned_data.dict())

    return templates.TemplateResponse("auth/signup.html", context)


@app.get("/users")
def user_list_view():
    return list(User.objects.all().limit(10))
