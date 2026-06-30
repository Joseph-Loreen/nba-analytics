from fastapi import FastAPI

app = FastAPI(title="NBA Analytics API")

@app.get("/")
def read_root():
    return {"message": "NBA Analytics API is running"}