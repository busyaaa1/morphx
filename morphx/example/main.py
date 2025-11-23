from fastapi import FastAPI
from morphx import morph
from pydantic import BaseModel

app = FastAPI(title="morphx demo")

class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create(data: list[dict]):
    users = morph(data, to=User)      # ← вот и вся магия
    return morph(users, to=dict)