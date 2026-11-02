"""
Teste determinístico de rotas FastAPI (tools/test_app_endpoints.py)
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_api():
    print("[Teste 1] GET / (Interface HTML)")
    res = client.get("/")
    assert res.status_code == 200
    assert "Gerenciador de Treino" in res.text
    print(" -> Frontend HTML servido com sucesso.")

    print("[Teste 2] GET /api/semana")
    res = client.get("/api/semana")
    assert res.status_code == 200
    dias = res.json()
    assert len(dias) == 7
    print(f" -> Resumo semanal validado: {len(dias)} dias retornados.")

    print("[Teste 3] GET /api/treino/Segunda-feira")
    res = client.get("/api/treino/Segunda-feira")
    assert res.status_code == 200
    treino = res.json()
    assert treino["dia_semana"] == "Segunda-feira"
    assert len(treino["exercicios"]) > 0
    print(f" -> Treino de Segunda: {treino['tipo_treino']}, {len(treino['exercicios'])} exercicios.")

    print("[Teste 4] POST /api/serie/executar")
    ex_id = treino["exercicios"][0]["exercicio_id"]
    res = client.post("/api/serie/executar", json={
        "exercicio_id": ex_id,
        "numero_serie": 2,
        "carga_kg": 72.5,
        "repeticoes": 10,
        "tecnica_avancada": "Nenhuma",
        "tempo_descanso_segundos": 90
    })
    assert res.status_code == 200
    assert res.json()["status"] == "sucesso"
    print(" -> Execucao de serie registrada via API.")

    print("[Teste 5] GET /api/metricas/exercicio/{id}")
    res = client.get(f"/api/metricas/exercicio/{ex_id}")
    assert res.status_code == 200
    metricas = res.json()
    assert metricas["status"] == "sucesso"
    assert metricas["kpis"]["carga_max_historica_kg"] >= 72.5
    print(f" -> Metricas da API OK: Carga Max = {metricas['kpis']['carga_max_historica_kg']} kg.")

    print("\n[OK] TODOS OS ENDPOINTS DA API RESPONDERAM 100% CORRETOS!")

if __name__ == "__main__":
    test_api()

