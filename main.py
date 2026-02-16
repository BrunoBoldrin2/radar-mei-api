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
