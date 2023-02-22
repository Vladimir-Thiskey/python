from fastapi import FastAPI
from scraper import Scraper
import uvicorn
from pydantic import BaseModel
from typing import List


class Pets(BaseModel):
    pet: str
    pet_name: str


class User(BaseModel):
    first_name: str
    second_name: str
    age: int
    gender: str
    pets: List[Pets]


app = FastAPI()
quotes = Scraper


@app.get("/")
def read_root():
    return {"HelloWorld": "Первая страница чего-нибудь"}


@app.get("/{cat}")
async def read_item(cat):
    return quotes.scrapedata(cat)


@app.get("/sum/{a}")
def calculate(a: int, b: int):
    return a + b


@app.post('/user')
def create_user(item: User):
    return item


if __name__ == "__main__":
    uvicorn.run("main:app", port=80, reload=True)
