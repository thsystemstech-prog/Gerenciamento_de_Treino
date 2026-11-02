# Gerenciador de Treino 🏋️‍♂️

Sistema determinístico e moderno para planejamento, acompanhamento e análise de treinos semanais. Desenvolvido sob o protocolo **V.L.A.E.G.** e arquitetura **A.N.T.** em 3 camadas.

---

## 🚀 Funcionalidades

- **Planejamento Semanal Completo:** Gestão de treinos de Segunda a Domingo com identificação de grupos musculares, divisão de treinos e observações.
- **Detalhamento de Séries e Técnicas Avançadas:** Suporte para Drop-set, Rest-pause, Bi-set, Tri-set, Pirâmides e intervalos de descanso configuráveis por série.
- **Execução em Tempo Real:**
  - Checkbox interativo para conclusão de séries.
  - Cronômetro regressivo de descanso sonoro com bips de contagem regressiva e aviso ao final.
- **Histórico e Gráficos de Evolução:** Métricas com evolução de carga máxima (kg) e volume total levantado (kg) por exercício com gráficos Chart.js.
- **Persistência Determinística:** SQLite local com integridade referencial, modo WAL e inicialização automática com dados de exemplo.

---

## 🛠️ Arquitetura (3 Camadas)

- **Camada 1 (Arquitetura):** Procedimentos Operacionais Padrão (POPs) técnicos em `architecture/`.
- **Camada 2 (Navegação/API):** Endpoints REST em `app.py` utilizando FastAPI.
- **Camada 3 (Ferramentas Atômicas):** Módulos determinísticos e testáveis em `tools/` (`db.py`, `treinos.py`, `metricas.py`, `seed_data.py`).

---

## 📦 Instalação e Execução

### Pré-requisitos
- Python 3.10+ instalado

### 1. Clonar o repositório
```bash
git clone https://github.com/thsystemstech-prog/Gerenciamento_de_Treino.git
cd Gerenciamento_de_Treino
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente (Opcional)
Copie o arquivo de exemplo caso queira customizar porta ou host:
```bash
cp .env.example .env
```

### 4. Iniciar a aplicação

**No Windows (clique duplo ou terminal):**
```bash
iniciar.bat
```
ou
```bash
python run.py
```

O navegador abrirá automaticamente em `http://127.0.0.1:8000`.

---

## 🧪 Execução de Testes

Os testes unitários das ferramentas e endpoints podem ser executados com:
```bash
python tools/test_tools.py
python tools/test_app_endpoints.py
```

---

## 📄 Licença
Distribuído sob a licença MIT.
