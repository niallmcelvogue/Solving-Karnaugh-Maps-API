from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from SolveKMap import main
from pydantic import BaseModel
from database import (
fetch_result,
add_result
)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    input: str


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/solve")
async def solve(x: Item):
    x = x.input
    x = x.split()
    x = list(map(int, x))
    result = main(x)
    response = await add_result(result.dict())
    if response:
        return response
    raise HTTPException(404, "Error adding result to DB")
