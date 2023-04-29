from cassandra.cqlengine.management import sync_table
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from starlette.middleware.authentication import AuthenticationMiddleware

from .users.backends import JWTCookieBackend
from .users.models import User
from . import db, utils
from .users.schemas import UserSignupSchema, UserLoginSchema
from .users.decorators import login_required
from .handlers import *  # noqa

from videos.models import Video
from videos.routers import router as video_router

DB_SESSION = None

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=JWTCookieBackend())
app.include_router(video_router)


@app.on_event("startup")
def on_startup():
    print("Hello World")
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)
    sync_table(Video)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    if request.user.is_authenticated:
        return render(request, "dashboard.html", {}, status_code=200)

    return render(request, "home.html")


@app.get("/account", response_class=HTMLResponse)
@login_required
def account_view(request: Request):
    return render(request, "account.html")


@app.get("/login", response_class=HTMLResponse)
def login_get_view(request: Request):
    session_id = request.cookies.get("session_id") or None
    return render(request, "auth/login.html", {
        "logged_in": session_id is not None
    })


@app.post("/login")
def login_post_view(
        request: Request,
        email: str = Form(...),
        password: str = Form(...)
):
    raw_data = {
        "email": email,
        "password": password,
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserLoginSchema)
    context = {
        "data": data,
        "errors": errors
    }
    if len(errors) > 0:
        return render(request, "auth/login.html", context, status_code=400)

    return redirect("/", cookies=data)


@app.get("/signup", response_class=HTMLResponse)
def signup_get_view(request: Request):
    return render(request, "auth/signup.html")


@app.post("/signup")
def signup_post_view(
        request: Request,
        email: str = Form(...),
        password: str = Form(...),
        password_confirm: str = Form(...)
):
    raw_data = {
        "email": email,
        "password": password,
        "password_confirm": password_confirm,
    }
    data, errors = utils.valid_schema_data_or_error(raw_data, UserSignupSchema)
    context = {
        "data": data,
        "errors": errors,
    }
    if len(errors) > 0:
        return render(request, "auth/signup.html", context, status_code=400)

    return redirect("/login")


@app.get("/users")
def user_list_view():
    return list(User.objects.all().limit(10))
