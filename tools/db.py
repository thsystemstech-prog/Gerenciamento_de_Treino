"""
Camada 3 - Ferramenta de Banco de Dados SQLite (tools/db.py)
POP de Referência: architecture/pop_db_manager.md
"""

import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def get_db_path() -> Path:
    db_env = os.getenv("DATABASE_PATH", "data/treinos.db")
    path = Path(db_env)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path

def get_connection() -> sqlite3.Connection:
    path = get_db_path()
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;")
    return conn

def init_db() -> None:
    """Cria as tabelas necessárias de forma determinística e idempotente."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS treinos_dia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dia_semana TEXT NOT NULL UNIQUE,
        tipo_treino TEXT NOT NULL,
        observacoes TEXT,
        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS exercicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        treino_dia_id INTEGER NOT NULL REFERENCES treinos_dia(id) ON DELETE CASCADE,
        nome TEXT NOT NULL,
        grupo_muscular TEXT NOT NULL,
        ordem INTEGER DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS series_planejadas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercicio_id INTEGER NOT NULL REFERENCES exercicios(id) ON DELETE CASCADE,
        numero_serie INTEGER NOT NULL,
        carga_kg REAL NOT NULL DEFAULT 0.0,
        repeticoes INTEGER NOT NULL DEFAULT 10,
        tecnica_avancada TEXT NOT NULL DEFAULT 'Nenhuma',
        tempo_descanso_segundos INTEGER NOT NULL DEFAULT 60
    );

    CREATE TABLE IF NOT EXISTS series_executadas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        exercicio_id INTEGER NOT NULL REFERENCES exercicios(id) ON DELETE CASCADE,
        numero_serie INTEGER NOT NULL,
        carga_kg REAL NOT NULL,
        repeticoes INTEGER NOT NULL,
        tecnica_avancada TEXT NOT NULL DEFAULT 'Nenhuma',
        tempo_descanso_segundos INTEGER NOT NULL,
        concluido INTEGER NOT NULL DEFAULT 1,
        executado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Banco de dados SQLite inicializado com sucesso!")

