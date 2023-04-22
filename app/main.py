from fastapi import FastAPI

from . import config, db
from app.users.models import User

from cassandra.cqlengine.management import sync_table

app = FastAPI()
DB_SESSION = None
settings = config.get_settings()


@app.on_event("startup")
def on_startup():
    print("Hello World")
    global DB_SESSION
    DB_SESSION = db.get_session()
    sync_table(User)


@app.get("/")
def homepage():
    return {"message": "Hello World"}


@app.get("/users")
def user_list_view():
    return list(User.objects.all().limit(10))