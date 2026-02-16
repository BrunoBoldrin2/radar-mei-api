from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://radar-mei-site.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

def criar_tabela():
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS analises (
                id SERIAL PRIMARY KEY,
                valor_mensal FLOAT,
                percentual_limite FLOAT,
                risco TEXT,
                criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.commit()

criar_tabela()


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

    # salvar no banco
    with engine.connect() as conn:
        conn.execute(
            text("""
                INSERT INTO analises (valor_mensal, percentual_limite, risco)
                VALUES (:valor, :percentual, :risco)
            """),
            {
                "valor": valor,
                "percentual": percentual_limite,
                "risco": risco
            }
        )
        conn.commit()

    return {
        "media_mensal": valor,
        "projecao_anual": round(projecao_anual, 2),
        "percentual_limite": round(percentual_limite, 2),
        "risco": risco
    }

