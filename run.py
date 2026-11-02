"""
Script de Inicialização do Gerenciador de Treino (run.py)
"""

import os
import sys
import webbrowser
from threading import Timer
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

load_dotenv()

def open_browser(url: str):
    try:
        webbrowser.open(url)
    except Exception:
        pass

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "8000"))
    url = f"http://{host}:{port}"

    print("=" * 60)
    print("⚡ GERENCIADOR DE TREINO - INICIANDO SISTEMA")
    print(f"🌐 Acesse no seu navegador: {url}")
    print("=" * 60)

    # Abre automaticamente no navegador após 1.2 segundos
    Timer(1.2, open_browser, args=[url]).start()

    uvicorn.run("app:app", host=host, port=port, reload=False)

