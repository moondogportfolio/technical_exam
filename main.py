from typing import Union
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from pymongo import MongoClient

from bson.json_util import dumps, loads
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

CONNECTION_STRING = "mongodb+srv://jaja:ALxMYwynp0QN9znO@cluster0.cngwc.mongodb.net/?retryWrites=true&w=majority"
db_name = "site"
collection_name = "kellywood"
print(CONNECTION_STRING)
client = MongoClient(CONNECTION_STRING)
db = client[db_name]
kelly = db[collection_name]


class SubmitForm(BaseModel):
    name: str
    email: str
    msg: str


origins = ["*"]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/form_submissions")
def get_submissions():
    cursor = kelly.find({}, {"_id": False})
    return loads(dumps(cursor))


@app.get("/{nav_button}")
def navigate(request: Request, nav_button: str):
    routes = {
        "about": "About Us",
        "services": "Services",
        "employment": "Employment",
        "contact": "Contact Us",
    }
    return templates.TemplateResponse(
        "other_routes.html",
        {"request": request, "titlename": routes[nav_button], "route": nav_button},
    )


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/submit")
def submit_form(data: SubmitForm):

    today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    kelly.insert_one(
        {"date": today, "message": data.msg, "name": data.name, "email": data.email}
    )
    return {"a": "ok"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
