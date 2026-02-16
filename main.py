from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"status": "Radar MEI API online"}


class AnaliseMEI(BaseModel):
    faturamentos: List[float]


@app.post("/analisar-mei")
def analisar_mei(dados: AnaliseMEI):

    limite = 81000

    faturamento_total = sum(dados.faturamentos)
    media_mensal = faturamento_total / len(dados.faturamentos)

    projecao_anual = media_mensal * 12
    percentual_limite = (projecao_anual / limite) * 100

    if percentual_limite >= 100:
        risco = "alto"
    elif percentual_limite >= 80:
        risco = "moderado"
    else:
        risco = "baixo"

    return {
        "faturamento_total": faturamento_total,
        "percentual_limite": round(percentual_limite, 2),
        "projecao_anual": round(projecao_anual, 2),
        "risco": risco
    }

@app.get("/simular")
def simular(valor: float):

    limite = 81000

    projecao_anual = valor * 12
    percentual_limite = (projecao_anual / limite) * 100

    if percentual_limite >= 100:
        risco = "alto"
    elif percentual_limite >= 80:
        risco = "moderado"
    else:
        risco = "baixo"

    return {
        "media_mensal": valor,
        "projecao_anual": round(projecao_anual, 2),
        "percentual_limite": round(percentual_limite, 2),
        "risco": risco
    }

