"""
Camada 3 - Ferramenta de Gerenciamento de Treinos (tools/treinos.py)
POP de Referência: architecture/pop_treino_service.md
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.db import get_connection

DIAS_SEMANA = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo"
]

TECNICAS_AVANCADAS = [
    "Nenhuma",
    "Drop-set",
    "Rest-pause",
    "Bi-set",
    "Tri-set",
    "Super-slow",
    "Pirâmide Crescente",
    "Pirâmide Decrescente",
    "Cluster Sets",
    "Pausa Isométrica"
]

def validar_dia_semana(dia_semana: str) -> None:
    if dia_semana not in DIAS_SEMANA:
        raise ValueError(f"Dia da semana inválido: '{dia_semana}'. Permitidos: {DIAS_SEMANA}")

def salvar_ou_atualizar_treino_dia(
    dia_semana: str,
    tipo_treino: str,
    observacoes: Optional[str],
    exercicios_payload: List[Dict[str, Any]]
) -> int:
    """
    Cadastra ou atualiza o planejamento de treino de um dia da semana.
    Usa transação atômica.
    """
    validar_dia_semana(dia_semana)
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # 1. Obter ou criar registro do dia
        cursor.execute("SELECT id FROM treinos_dia WHERE dia_semana = ?", (dia_semana,))
        row = cursor.fetchone()

        if row:
            treino_dia_id = row["id"]
            cursor.execute(
                "UPDATE treinos_dia SET tipo_treino = ?, observacoes = ? WHERE id = ?",
                (tipo_treino, observacoes, treino_dia_id)
            )
            # Remove exercícios antigos do plano
            cursor.execute("DELETE FROM exercicios WHERE treino_dia_id = ?", (treino_dia_id,))
        else:
            cursor.execute(
                "INSERT INTO treinos_dia (dia_semana, tipo_treino, observacoes) VALUES (?, ?, ?)",
                (dia_semana, tipo_treino, observacoes)
            )
            treino_dia_id = cursor.lastrowid

        # 2. Inserir exercícios e séries planejadas
        for idx, ex in enumerate(exercicios_payload, start=1):
            nome = ex.get("nome", "").strip()
            if not nome:
                continue
            grupo = ex.get("grupo_muscular", "Geral").strip()

            cursor.execute(
                "INSERT INTO exercicios (treino_dia_id, nome, grupo_muscular, ordem) VALUES (?, ?, ?, ?)",
                (treino_dia_id, nome, grupo, idx)
            )
            exercicio_id = cursor.lastrowid

            series = ex.get("series", [])
            for s_idx, s in enumerate(series, start=1):
                carga = float(s.get("carga_kg", 0.0))
                reps = int(s.get("repeticoes", 10))
                tecnica = s.get("tecnica_avancada", "Nenhuma")
                descanso = int(s.get("tempo_descanso_segundos", 60))

                cursor.execute(
                    """
                    INSERT INTO series_planejadas
                    (exercicio_id, numero_serie, carga_kg, repeticoes, tecnica_avancada, tempo_descanso_segundos)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (exercicio_id, s_idx, carga, reps, tecnica, descanso)
                )

        conn.commit()
        return treino_dia_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def obter_resumo_semanal() -> List[Dict[str, Any]]:
    """Retorna o panorama dos 7 dias da semana."""
    conn = get_connection()
    cursor = conn.cursor()

    resumo = []
    for dia in DIAS_SEMANA:
        cursor.execute("""
            SELECT td.id, td.tipo_treino, td.observacoes,
                   COUNT(DISTINCT e.id) as total_exercicios,
                   COUNT(sp.id) as total_series,
                   SUM(sp.tempo_descanso_segundos) as descanso_total_seg
            FROM treinos_dia td
            LEFT JOIN exercicios e ON e.treino_dia_id = td.id
            LEFT JOIN series_planejadas sp ON sp.exercicio_id = e.id
            WHERE td.dia_semana = ?
            GROUP BY td.id
        """, (dia,))
        row = cursor.fetchone()

        if row and row["id"]:
            descanso_seg = row["descanso_total_seg"] or 0
            # Estimativa: tempo de descanso + 40s de execução por série
            tempo_estimado_min = round((descanso_seg + (row["total_series"] * 40)) / 60, 1)
            resumo.append({
                "dia_semana": dia,
                "tem_treino": True,
                "treino_id": row["id"],
                "tipo_treino": row["tipo_treino"],
                "observacoes": row["observacoes"] or "",
                "total_exercicios": row["total_exercicios"],
                "total_series": row["total_series"],
                "tempo_estimado_min": tempo_estimado_min
            })
        else:
            resumo.append({
                "dia_semana": dia,
                "tem_treino": False,
                "treino_id": None,
                "tipo_treino": "Descanso / Livre",
                "observacoes": "Nenhum treino programado",
                "total_exercicios": 0,
                "total_series": 0,
                "tempo_estimado_min": 0
            })

    conn.close()
    return resumo

def obter_treino_dia(dia_semana: str) -> Optional[Dict[str, Any]]:
    """Retorna os dados completos do treino de um dia, com exercícios e séries planejadas + execuções."""
    validar_dia_semana(dia_semana)
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM treinos_dia WHERE dia_semana = ?", (dia_semana,))
    t_row = cursor.fetchone()

    if not t_row:
        conn.close()
        return None

    treino_dia_id = t_row["id"]

    cursor.execute("SELECT * FROM exercicios WHERE treino_dia_id = ? ORDER BY ordem, id", (treino_dia_id,))
    ex_rows = cursor.fetchall()

    exercicios = []
    total_series = 0
    descanso_total_seg = 0

    hoje_str = datetime.now().strftime("%Y-%m-%d")

    for ex in ex_rows:
        ex_id = ex["id"]
        # Buscar séries planejadas
        cursor.execute("SELECT * FROM series_planejadas WHERE exercicio_id = ? ORDER BY numero_serie", (ex_id,))
        sp_rows = cursor.fetchall()

        # Buscar séries executadas hoje
        cursor.execute(
            """
            SELECT * FROM series_executadas
            WHERE exercicio_id = ? AND date(executado_em) = date('now', 'localtime')
            ORDER BY numero_serie
            """,
            (ex_id,)
        )
        se_rows = cursor.fetchall()
        executadas_map = {row["numero_serie"]: dict(row) for row in se_rows}

        series = []
        for sp in sp_rows:
            num = sp["numero_serie"]
            executada = executadas_map.get(num)
            total_series += 1
            descanso_total_seg += sp["tempo_descanso_segundos"]

            series.append({
                "serie_planejada_id": sp["id"],
                "numero_serie": num,
                "carga_sugerida_kg": sp["carga_kg"],
                "repeticoes_sugeridas": sp["repeticoes"],
                "tecnica_avancada": sp["tecnica_avancada"],
                "tempo_descanso_segundos": sp["tempo_descanso_segundos"],
                "concluido": bool(executada),
                "execucao_real": executada if executada else None
            })

        exercicios.append({
            "exercicio_id": ex_id,
            "nome": ex["nome"],
            "grupo_muscular": ex["grupo_muscular"],
            "ordem": ex["ordem"],
            "series": series
        })

    tempo_estimado_min = round((descanso_total_seg + (total_series * 40)) / 60, 1)

    resultado = {
        "id": treino_dia_id,
        "dia_semana": dia_semana,
        "tipo_treino": t_row["tipo_treino"],
        "observacoes": t_row["observacoes"] or "",
        "total_exercicios": len(exercicios),
        "total_series": total_series,
        "tempo_total_estimado_min": tempo_estimado_min,
        "exercicios": exercicios
    }

    conn.close()
    return resultado

def registrar_execucao_serie(
    exercicio_id: int,
    numero_serie: int,
    carga_kg: float,
    repeticoes: int,
    tecnica_avancada: str = "Nenhuma",
    tempo_descanso_segundos: int = 60
) -> Dict[str, Any]:
    """Registra uma série executada no banco de dados."""
    if carga_kg < 0:
        raise ValueError("Carga não pode ser negativa")
    if repeticoes < 1:
        raise ValueError("Repetições devem ser maiores ou iguais a 1")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO series_executadas
        (exercicio_id, numero_serie, carga_kg, repeticoes, tecnica_avancada, tempo_descanso_segundos, concluido)
        VALUES (?, ?, ?, ?, ?, ?, 1)
    """, (exercicio_id, numero_serie, carga_kg, repeticoes, tecnica_avancada, tempo_descanso_segundos))

    serie_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "status": "sucesso",
        "serie_id": serie_id,
        "exercicio_id": exercicio_id,
        "numero_serie": numero_serie,
        "tempo_descanso_recomendado": tempo_descanso_segundos,
        "mensagem": f"Série {numero_serie} registrada com sucesso!"
    }

def listar_todos_exercicios() -> List[Dict[str, Any]]:
    """Retorna lista com todos os exercícios cadastrados no sistema."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, e.nome, e.grupo_muscular, td.dia_semana, td.tipo_treino
        FROM exercicios e
        JOIN treinos_dia td ON td.id = e.treino_dia_id
        ORDER BY e.nome
    """)
    rows = cursor.fetchall()
    exercicios = [dict(r) for r in rows]
    conn.close()
    return exercicios
