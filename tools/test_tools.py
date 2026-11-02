"""
Teste Unitário Determinístico das Ferramentas da Camada 3 (tools/test_tools.py)
"""

import sys
from pathlib import Path

# Garante inclusão do diretório raiz no sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from tools.db import init_db
from tools.treinos import (
    obter_resumo_semanal,
    obter_treino_dia,
    registrar_execucao_serie,
    salvar_ou_atualizar_treino_dia
)
from tools.metricas import calcular_metricas_exercicio
from tools.seed_data import popular_banco_se_vazio

def run_tests():
    print("[Teste 1] Inicialização do banco de dados...")
    init_db()

    print("[Teste 2] Carga de dados inicial (Seed)...")
    popular_banco_se_vazio()

    print("[Teste 3] Resumo semanal...")
    resumo = obter_resumo_semanal()
    assert len(resumo) == 7, f"Esperado 7 dias, recebido {len(resumo)}"
    segunda = next(r for r in resumo if r["dia_semana"] == "Segunda-feira")
    assert segunda["tem_treino"] is True
    assert segunda["total_exercicios"] >= 1
    print(f" -> Resumo semanal OK: Segunda tem {segunda['total_exercicios']} exercicios e {segunda['total_series']} series.")

    print("[Teste 4] Detalhes do treino do dia...")
    treino_seg = obter_treino_dia("Segunda-feira")
    assert treino_seg is not None
    assert len(treino_seg["exercicios"]) > 0
    primeiro_ex = treino_seg["exercicios"][0]
    print(f" -> Treino carregado: {primeiro_ex['nome']} ({len(primeiro_ex['series'])} series planejadas).")

    print("[Teste 5] Registro de execução de série...")
    ex_id = primeiro_ex["exercicio_id"]
    res_exec = registrar_execucao_serie(
        exercicio_id=ex_id,
        numero_serie=1,
        carga_kg=62.5,
        repeticoes=12,
        tecnica_avancada="Nenhuma",
        tempo_descanso_segundos=90
    )
    assert res_exec["status"] == "sucesso"
    assert res_exec["tempo_descanso_recomendado"] == 90
    print(" -> Execucao registrada com sucesso!")

    print("[Teste 6] Calculo de metricas e progressao...")
    metricas = calcular_metricas_exercicio(ex_id)
    assert metricas["status"] == "sucesso"
    assert len(metricas["historico"]) >= 1
    assert metricas["kpis"]["carga_max_historica_kg"] >= 62.5
    print(f" -> Metricas OK: Carga Max = {metricas['kpis']['carga_max_historica_kg']} kg, Volume = {metricas['kpis']['volume_total_acumulado_kg']} kg.")

    print("\n[OK] TODOS OS TESTES DETERMINISTICOS PASSARAM COM SUCESSO!")

if __name__ == "__main__":
    run_tests()
