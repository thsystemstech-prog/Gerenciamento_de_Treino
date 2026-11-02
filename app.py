"""
Aplicação Principal FastAPI - Gerenciador de Treino
Protocolo V.L.A.E.G. & Arquitetura A.N.T. em 3 Camadas
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

# Garante path de execução
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from tools.db import init_db
from tools.treinos import (
    DIAS_SEMANA,
    obter_resumo_semanal,
    obter_treino_dia,
    salvar_ou_atualizar_treino_dia,
    registrar_execucao_serie,
    listar_todos_exercicios
)
from tools.metricas import calcular_metricas_exercicio
from tools.seed_data import popular_banco_se_vazio, EXEMPLOS_TREINO

load_dotenv()

app = FastAPI(
    title="Gerenciador de Treino",
    description="Aplicativo determinístico para planejamento e acompanhamento de treinos semanais.",
    version="1.0.0"
)

# Inicialização automática do banco e seeds na subida da aplicação
@app.on_event("startup")
def startup_event():
    init_db()
    popular_banco_se_vazio()

# --- MODELOS PYDANTIC PARA VALIDAÇÃO DE ENTRADA ---
class SerieInput(BaseModel):
    numero_serie: Optional[int] = None
    carga_kg: float = Field(default=0.0, ge=0.0)
    repeticoes: int = Field(default=10, ge=1)
    tecnica_avancada: str = "Nenhuma"
    tempo_descanso_segundos: int = Field(default=60, ge=0)

class ExercicioInput(BaseModel):
    nome: str
    grupo_muscular: str = "Geral"
    series: List[SerieInput] = []

class TreinoDiaInput(BaseModel):
    dia_semana: str
    tipo_treino: str
    observacoes: Optional[str] = None
    exercicios: List[ExercicioInput] = []

class ExecucaoSerieInput(BaseModel):
    exercicio_id: int
    numero_serie: int
    carga_kg: float = Field(ge=0.0)
    repeticoes: int = Field(ge=1)
    tecnica_avancada: str = "Nenhuma"
    tempo_descanso_segundos: int = 60

# --- ROTAS DA API ---

@app.get("/", response_class=HTMLResponse)
def index_page():
    template_path = BASE_DIR / "templates" / "index.html"
    if not template_path.exists():
        raise HTTPException(status_code=404, detail="Interface HTML não encontrada.")
    return HTMLResponse(content=template_path.read_text(encoding="utf-8"))

@app.get("/api/semana")
def get_semana():
    """Retorna o panorama dos 7 dias da semana."""
    return obter_resumo_semanal()

@app.get("/api/treino/{dia_semana}")
def get_treino(dia_semana: str):
    """Retorna detalhes do treino do dia especificado."""
    if dia_semana not in DIAS_SEMANA:
        raise HTTPException(status_code=400, detail=f"Dia da semana inválido: {dia_semana}")
    
    treino = obter_treino_dia(dia_semana)
    if not treino:
        return {
            "id": None,
            "dia_semana": dia_semana,
            "tipo_treino": "Descanso / Vazio",
            "observacoes": "",
            "total_exercicios": 0,
            "total_series": 0,
            "tempo_total_estimado_min": 0,
            "exercicios": []
        }
    return treino

@app.post("/api/treino/{dia_semana}")
def salvar_treino(dia_semana: str, payload: TreinoDiaInput):
    """Cadastra ou atualiza o planejamento de treino de um dia."""
    if dia_semana not in DIAS_SEMANA:
        raise HTTPException(status_code=400, detail=f"Dia da semana inválido: {dia_semana}")
    
    try:
        exercicios_dict = [ex.model_dump() for ex in payload.exercicios]
        treino_id = salvar_ou_atualizar_treino_dia(
            dia_semana=dia_semana,
            tipo_treino=payload.tipo_treino,
            observacoes=payload.observacoes,
            exercicios_payload=exercicios_dict
        )
        return {
            "status": "sucesso",
            "mensagem": f"Treino de {dia_semana} salvo com sucesso!",
            "treino_id": treino_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/serie/executar")
def executar_serie(payload: ExecucaoSerieInput):
    """Registra uma série executada no treino do dia."""
    try:
        resultado = registrar_execucao_serie(
            exercicio_id=payload.exercicio_id,
            numero_serie=payload.numero_serie,
            carga_kg=payload.carga_kg,
            repeticoes=payload.repeticoes,
            tecnica_avancada=payload.tecnica_avancada,
            tempo_descanso_segundos=payload.tempo_descanso_segundos
        )
        return resultado
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/exercicios")
def get_exercicios():
    """Lista todos os exercícios existentes no sistema."""
    return listar_todos_exercicios()

@app.get("/api/metricas/exercicio/{exercicio_id}")
def get_metricas(exercicio_id: int):
    """Retorna dados de evolução e métricas para gráficos."""
    return calcular_metricas_exercicio(exercicio_id)

@app.post("/api/seed/reset")
def reset_seed():
    """Restaura a rotina exemplo."""
    for t in EXEMPLOS_TREINO:
        salvar_ou_atualizar_treino_dia(
            dia_semana=t["dia_semana"],
            tipo_treino=t["tipo_treino"],
            observacoes=t["observacoes"],
            exercicios_payload=t["exercicios"]
        )
    return {"status": "sucesso", "mensagem": "Rotina exemplo restaurada."}

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "8000"))
    print(f"Iniciando Gerenciador de Treino em http://{host}:{port} ...")
    uvicorn.run("app:app", host=host, port=port, reload=True)

