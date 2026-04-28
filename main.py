from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}


@app.get("/name/{name}")
def greet_name(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/add/{number}")
def add_number(number: int):
    result = number + 1
    return {
        "input": number,
        "operation": "add 1",
        "result": result
    }


@app.get("/double/{number}")
def double_number(number: int):
    result = number * 2
    return {
        "input": number,
        "operation": "double",
        "result": result
    }

