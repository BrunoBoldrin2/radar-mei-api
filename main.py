from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Radar MEI API online"}

@app.get("/calcular")
def calcular(valor: float):
    limite = 81000
    percentual = valor / limite

    return {
        "percentual_limite": round(percentual * 100, 2),
        "risco": "alto" if percentual > 0.8 else "ok"
    }

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
