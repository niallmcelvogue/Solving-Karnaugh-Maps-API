from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from SolveKMap import main as Solve
from test_handwriting import main as Extract
from pydantic import BaseModel
import base64


def decode_image(img):
    with open('imageToSave.png', 'wb') as fh:
        # Get only relevant data, deleting "data:image/png;base64,"
        data = img.split(',', 1)[1]
        fh.write(base64.b64decode(data))


def returnSolution(minterms):
    try:
        value = Solve(list(map(int, minterms.input.split())), minterms.noVar, minterms.type)
        if value is None:
            print("Error occurred")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Error solving input")
    result = {'output': value}
    return result


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
    noVar: int
    type: str

class Image(BaseModel):
    input: str
    type: str

@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/solve")
async def solve(minterms: Item):
    return returnSolution(minterms)


@app.post("/extract")
async def solve(img: Image):
    try:
        decode_image(img.input)
        return Extract(img.type)
    except:
        print("Error")
        raise HTTPException(status_code=400, detail="Error solving image")

