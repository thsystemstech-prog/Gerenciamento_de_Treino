"""
Camada 3 - Ferramenta de Métricas e Progressão de Carga (tools/metricas.py)
POP de Referência: architecture/pop_metricas_progressao.md
"""

from typing import Dict, Any, List
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.db import get_connection

def calcular_metricas_exercicio(exercicio_id: int) -> Dict[str, Any]:
    """
    Retorna métricas históricas agregadas e série temporal para gráficos
    de evolução de carga e volume por exercício.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Informações básicas do exercício
    cursor.execute("""
        SELECT e.id, e.nome, e.grupo_muscular, td.dia_semana, td.tipo_treino
        FROM exercicios e
        JOIN treinos_dia td ON td.id = e.treino_dia_id
        WHERE e.id = ?
    """, (exercicio_id,))
    ex_info = cursor.fetchone()

    if not ex_info:
        conn.close()
        return {
            "status": "vazio",
            "exercicio": None,
            "historico": [],
            "kpis": {
                "carga_max_historica_kg": 0.0,
                "volume_total_acumulado_kg": 0.0,
                "total_series_concluidas": 0,
                "maior_1rm_estimado": 0.0
            }
        }

    # 2. Séries executadas agrupadas por dia
    cursor.execute("""
        SELECT 
            date(executado_em) as data_execucao,
            MAX(carga_kg) as carga_max_kg,
            SUM(carga_kg * repeticoes) as volume_total_kg,
            SUM(repeticoes) as repeticoes_totais,
            COUNT(id) as total_series,
            MAX(carga_kg * (1.0 + (repeticoes / 30.0))) as um_rm_estimado
        FROM series_executadas
        WHERE exercicio_id = ?
        GROUP BY date(executado_em)
        ORDER BY date(executado_em) ASC
    """, (exercicio_id,))
    rows = cursor.fetchall()

    historico: List[Dict[str, Any]] = []
    carga_max_absoluta = 0.0
    volume_acumulado = 0.0
    total_series_geral = 0
    maior_1rm_absoluto = 0.0

    for r in rows:
        c_max = float(r["carga_max_kg"])
        vol = round(float(r["volume_total_kg"]), 1)
        reps = int(r["repeticoes_totais"])
        series_cnt = int(r["total_series"])
        um_rm = round(float(r["um_rm_estimado"]), 1)

        if c_max > carga_max_absoluta:
            carga_max_absoluta = c_max
        if um_rm > maior_1rm_absoluto:
            maior_1rm_absoluto = um_rm
        volume_acumulado += vol
        total_series_geral += series_cnt

        historico.append({
            "data": r["data_execucao"],
            "carga_max_kg": c_max,
            "volume_total_kg": vol,
            "repeticoes_totais": reps,
            "total_series": series_cnt,
            "um_rm_estimado": um_rm
        })

    conn.close()

    return {
        "status": "sucesso",
        "exercicio": {
            "id": ex_info["id"],
            "nome": ex_info["nome"],
            "grupo_muscular": ex_info["grupo_muscular"],
            "dia_semana": ex_info["dia_semana"],
            "tipo_treino": ex_info["tipo_treino"]
        },
        "historico": historico,
        "kpis": {
            "carga_max_historica_kg": carga_max_absoluta,
            "volume_total_acumulado_kg": round(volume_acumulado, 1),
            "total_series_concluidas": total_series_geral,
            "maior_1rm_estimado": maior_1rm_absoluto
        }
    }
