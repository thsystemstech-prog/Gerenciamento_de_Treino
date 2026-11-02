"""
Camada 3 - Ferramenta de Carga Inicial de Dados (tools/seed_data.py)
Preenche uma rotina semanal exemplar caso o banco esteja vazio.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.db import init_db, get_connection
from tools.treinos import salvar_ou_atualizar_treino_dia

EXEMPLOS_TREINO = [
    {
        "dia_semana": "Segunda-feira",
        "tipo_treino": "Push A (Peito, Ombros e Tríceps)",
        "observacoes": "Foco em progressão no supino e controle da fase excêntrica.",
        "exercicios": [
            {
                "nome": "Supino Reto com Barra",
                "grupo_muscular": "Peitoral",
                "series": [
                    {"numero_serie": 1, "carga_kg": 60.0, "repeticoes": 12, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 90},
                    {"numero_serie": 2, "carga_kg": 70.0, "repeticoes": 10, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 90},
                    {"numero_serie": 3, "carga_kg": 80.0, "repeticoes": 8, "tecnica_avancada": "Pirâmide Crescente", "tempo_descanso_segundos": 120},
                    {"numero_serie": 4, "carga_kg": 85.0, "repeticoes": 6, "tecnica_avancada": "Drop-set", "tempo_descanso_segundos": 120}
                ]
            },
            {
                "nome": "Desenvolvimento Halteres",
                "grupo_muscular": "Ombros",
                "series": [
                    {"numero_serie": 1, "carga_kg": 20.0, "repeticoes": 12, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 60},
                    {"numero_serie": 2, "carga_kg": 22.0, "repeticoes": 10, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 60},
                    {"numero_serie": 3, "carga_kg": 24.0, "repeticoes": 8, "tecnica_avancada": "Rest-pause", "tempo_descanso_segundos": 90}
                ]
            },
            {
                "nome": "Tríceps Corda na Polia",
                "grupo_muscular": "Tríceps",
                "series": [
                    {"numero_serie": 1, "carga_kg": 25.0, "repeticoes": 15, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 45},
                    {"numero_serie": 2, "carga_kg": 30.0, "repeticoes": 12, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 45},
                    {"numero_serie": 3, "carga_kg": 35.0, "repeticoes": 10, "tecnica_avancada": "Pausa Isométrica", "tempo_descanso_segundos": 60}
                ]
            }
        ]
    },
    {
        "dia_semana": "Terça-feira",
        "tipo_treino": "Pull A (Costas, Trapézio e Bíceps)",
        "observacoes": "Foco em ativação de grande dorsal e remadas pesadas.",
        "exercicios": [
            {
                "nome": "Puxada Frontal na Polia",
                "grupo_muscular": "Costas",
                "series": [
                    {"numero_serie": 1, "carga_kg": 50.0, "repeticoes": 12, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 60},
                    {"numero_serie": 2, "carga_kg": 60.0, "repeticoes": 10, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 90},
                    {"numero_serie": 3, "carga_kg": 70.0, "repeticoes": 8, "tecnica_avancada": "Drop-set", "tempo_descanso_segundos": 90}
                ]
            },
            {
                "nome": "Remada Curvada com Barra",
                "grupo_muscular": "Costas",
                "series": [
                    {"numero_serie": 1, "carga_kg": 40.0, "repeticoes": 10, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 90},
                    {"numero_serie": 2, "carga_kg": 50.0, "repeticoes": 8, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 90},
                    {"numero_serie": 3, "carga_kg": 60.0, "repeticoes": 6, "tecnica_avancada": "Cluster Sets", "tempo_descanso_segundos": 120}
                ]
            },
            {
                "nome": "Rosca Direta W",
                "grupo_muscular": "Bíceps",
                "series": [
                    {"numero_serie": 1, "carga_kg": 15.0, "repeticoes": 12, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 60},
                    {"numero_serie": 2, "carga_kg": 18.0, "repeticoes": 10, "tecnica_avancada": "Super-slow", "tempo_descanso_segundos": 60},
                    {"numero_serie": 3, "carga_kg": 20.0, "repeticoes": 8, "tecnica_avancada": "Drop-set", "tempo_descanso_segundos": 60}
                ]
            }
        ]
    },
    {
        "dia_semana": "Quarta-feira",
        "tipo_treino": "Legs A (Quadríceps e Panturrilhas)",
        "observacoes": "Agachamento profundo com postura alinhada.",
        "exercicios": [
            {
                "nome": "Agachamento Livre",
                "grupo_muscular": "Quadríceps",
                "series": [
                    {"numero_serie": 1, "carga_kg": 60.0, "repeticoes": 12, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 90},
                    {"numero_serie": 2, "carga_kg": 80.0, "repeticoes": 10, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 120},
                    {"numero_serie": 3, "carga_kg": 100.0, "repeticoes": 8, "tecnica_avancada": "Pirâmide Crescente", "tempo_descanso_segundos": 120}
                ]
            },
            {
                "nome": "Leg Press 45°",
                "grupo_muscular": "Quadríceps",
                "series": [
                    {"numero_serie": 1, "carga_kg": 140.0, "repeticoes": 12, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 90},
                    {"numero_serie": 2, "carga_kg": 180.0, "repeticoes": 10, "tecnica_avancada": "Rest-pause", "tempo_descanso_segundos": 90}
                ]
            },
            {
                "nome": "Gêmeos Sentado",
                "grupo_muscular": "Panturrilhas",
                "series": [
                    {"numero_serie": 1, "carga_kg": 35.0, "repeticoes": 15, "tecnica_avancada": "Pausa Isométrica", "tempo_descanso_segundos": 45},
                    {"numero_serie": 2, "carga_kg": 40.0, "repeticoes": 15, "tecnica_avancada": "Pausa Isométrica", "tempo_descanso_segundos": 45}
                ]
            }
        ]
    },
    {
        "dia_semana": "Quinta-feira",
        "tipo_treino": "Descanso Ativo / Mobilidade",
        "observacoes": "Alongamento global, caminhada leve ou descanso completo.",
        "exercicios": []
    },
    {
        "dia_semana": "Sexta-feira",
        "tipo_treino": "Upper B (Membros Superiores Foco Volume)",
        "observacoes": "Ênfase em densidade muscular e pump.",
        "exercicios": [
            {
                "nome": "Supino Inclinado com Halteres",
                "grupo_muscular": "Peitoral",
                "series": [
                    {"numero_serie": 1, "carga_kg": 24.0, "repeticoes": 12, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 60},
                    {"numero_serie": 2, "carga_kg": 28.0, "repeticoes": 10, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 90},
                    {"numero_serie": 3, "carga_kg": 30.0, "repeticoes": 8, "tecnica_avancada": "Drop-set", "tempo_descanso_segundos": 90}
                ]
            },
            {
                "nome": "Elevação Lateral com Halteres",
                "grupo_muscular": "Ombros",
                "series": [
                    {"numero_serie": 1, "carga_kg": 10.0, "repeticoes": 15, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 45},
                    {"numero_serie": 2, "carga_kg": 12.0, "repeticoes": 12, "tecnica_avancada": "Rest-pause", "tempo_descanso_segundos": 45}
                ]
            }
        ]
    },
    {
        "dia_semana": "Sábado",
        "tipo_treino": "Lower B (Posterior de Coxa, Glúteos e Abdômen)",
        "observacoes": "Levantamento terra ou stiff com técnica refinada.",
        "exercicios": [
            {
                "nome": "Stiff com Barra",
                "grupo_muscular": "Posterior",
                "series": [
                    {"numero_serie": 1, "carga_kg": 40.0, "repeticoes": 12, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 90},
                    {"numero_serie": 2, "carga_kg": 50.0, "repeticoes": 10, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 90}
                ]
            },
            {
                "nome": "Abdominal Supra na Polia",
                "grupo_muscular": "Abdômen",
                "series": [
                    {"numero_serie": 1, "carga_kg": 30.0, "repeticoes": 20, "tecnica_avancada": "Nenhuma", "tempo_descanso_segundos": 45},
                    {"numero_serie": 2, "carga_kg": 35.0, "repeticoes": 15, "tecnica_avancada": "Pausa Isométrica", "tempo_descanso_segundos": 45}
                ]
            }
        ]
    },
    {
        "dia_semana": "Domingo",
        "tipo_treino": "Descanso Total / Recuperação",
        "observacoes": "Hidratação, sono adequado e alimentação regenerativa.",
        "exercicios": []
    }
]

def popular_banco_se_vazio() -> bool:
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM treinos_dia")
    row = cursor.fetchone()
    total = row["total"] if row else 0
    conn.close()

    if total == 0:
        for t in EXEMPLOS_TREINO:
            salvar_ou_atualizar_treino_dia(
                dia_semana=t["dia_semana"],
                tipo_treino=t["tipo_treino"],
                observacoes=t["observacoes"],
                exercicios_payload=t["exercicios"]
            )
        return True
    return False

if __name__ == "__main__":
    populado = popular_banco_se_vazio()
    if populado:
        print("Dados exemplares inseridos com sucesso!")
    else:
        print("Banco já continha treinos cadastrados.")
