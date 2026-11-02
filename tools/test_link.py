"""
Script de verificação de Link e Handshake (Fase 2 - Link).
Testa a conectividade com as variáveis de ambiente, diretórios e motor SQLite.
"""

import os
import sys
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def test_environment() -> bool:
    print("[1/5] Carregando .env...")
    load_dotenv()
    db_path = os.getenv("DATABASE_PATH", "data/treinos.db")
    print(f" -> DATABASE_PATH: {db_path}")

    print("[2/5] Verificando pasta temporária .tmp/...")
    tmp_dir = Path(".tmp")
    tmp_dir.mkdir(exist_ok=True)
    test_tmp_file = tmp_dir / "handshake_test.tmp"
    test_tmp_file.write_text("handshake ok", encoding="utf-8")
    assert test_tmp_file.read_text(encoding="utf-8") == "handshake ok"
    test_tmp_file.unlink()
    print(" -> .tmp/ operacional e determinística.")

    print("[3/5] Verificando diretório do banco de dados...")
    db_file = Path(db_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)
    print(f" -> Diretório {db_file.parent} pronto.")

    print("[4/5] Testando handshake com SQLite...")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS _handshake_test (id INTEGER PRIMARY KEY, ping TEXT);")
    cursor.execute("INSERT INTO _handshake_test (ping) VALUES ('pong');")
    conn.commit()
    cursor.execute("SELECT ping FROM _handshake_test ORDER BY id DESC LIMIT 1;")
    result = cursor.fetchone()
    cursor.execute("DROP TABLE _handshake_test;")
    conn.commit()
    conn.close()
    assert result and result[0] == "pong"
    print(" -> SQLite handshake bem-sucedido (ping/pong OK).")

    print("[5/5] Verificando módulos de runtime...")
    import fastapi
    import uvicorn
    import pydantic
    print(f" -> FastAPI v{fastapi.__version__}")
    print(f" -> Uvicorn v{uvicorn.__version__}")
    print(f" -> Pydantic v{pydantic.__version__}")

    print("\n✅ TODOS OS TESTES DA FASE 2 (LINK) PASSARAM COM SUCESSO!")
    return True

if __name__ == "__main__":
    success = test_environment()
    sys.exit(0 if success else 1)
