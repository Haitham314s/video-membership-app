from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def homepage():
    return {"message": "Hello World"}
