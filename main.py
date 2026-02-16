from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Radar MEI API online"}
