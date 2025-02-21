from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"Hello": "lala"}

@app.get("/quadrado/{num}")
def square(num: int):
    return num ** 2
