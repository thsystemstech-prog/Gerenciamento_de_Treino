# Plano de Tarefas (Task Plan) - Gerenciador de Treino

## Status do Projeto
- **Fase Atual:** Projeto Concluído com Sucesso! 🚀
- **Status:** Todas as 5 fases do Protocolo V.L.A.E.G. foram executadas, validadas e testadas deterministamente.

---

## Blueprint da Arquitetura (A.N.T. em 3 Camadas)

### 1. Camada 1: Arquitetura (`architecture/`)
- `architecture/pop_db_manager.md`: POP para inicialização, migrações e operações de CRUD no SQLite (`data/treinos.db`).
- `architecture/pop_treino_service.md`: POP para regras de negócio de planejamento semanal, montagem de treinos, cálculo de volume de treino e progressão de carga.
- `architecture/pop_web_ui.md`: POP para a interface web (páginas/rotas: Planejamento Semanal, Modo Treino com Timer e Dashboard de Evolução).

### 2. Camada 2: Navegação & Orquestração
- Coordenação de fluxos de dados entre a interface e os scripts de execução determinística.
- Garantia de que nenhuma regra de negócio opere de forma probabilística.

### 3. Camada 3: Ferramentas Determinísticas (`tools/`)
- `tools/db.py`: Módulo atômico de conexão e operações no SQLite.
- `tools/treinos.py`: Funções para registrar, listar e atualizar treinos semanais e séries.
- `tools/metricas.py`: Funções determinísticas para calcular histórico de volume (Carga x Repetições), carga máxima e métricas de evolução.
- `app.py`: Interface Web interativa (Streamlit ou FastAPI Web UI) contendo:
  - **Aba 1: Calendário Semanal:** Visualização dos dias da semana (Segunda a Domingo) com o treino programado e botão para cadastrar/editar exercícios.
  - **Aba 2: Modo Execução (Treino do Dia):** Check-in de séries com carga real, repetições, técnica avançada e **Cronômetro Interativo de Descanso** com aviso sonoro.
  - **Aba 3: Evolução & Gráficos:** Gráficos interativos de progressão de carga e volume por exercício.

---

## Fases do Protocolo V.L.A.E.G.

### Fase 0: Inicialização (Concluída)
- [x] Criar arquivos de memória do projeto (`task_plan.md`, `findings.md`, `progress.md`).
- [x] Criar constituição do projeto (`gemini.md`).
- [x] Criar estrutura básica de diretórios (`architecture/`, `tools/`, `.tmp/`).

### Fase 1: V - Visão (e Lógica)
- [x] Coleta de respostas das 5 Perguntas de Descoberta.
- [x] Definição do Esquema de Dados (JSON Data Schema) de Entrada e Saída em `gemini.md`.
- [x] Elaboração do Blueprint da Arquitetura.
- [x] **Aprovação do Blueprint pelo usuário (Gate obrigatório antes do código).**

### Fase 2: L - Link (Conectividade)
- [x] Configuração do ambiente Python e dependências (`requirements.txt`).
- [x] Criação de script de verificação do ambiente e SQLite local em `tools/`.
- [x] Execução do handshake completo com sucesso.

### Fase 3: A - Arquitetura (Construção em 3 Camadas)
- [x] Camada 1: Escrever POPs técnicos em `architecture/`.
- [x] Camada 3: Implementar scripts determinísticos em `tools/` (`db.py`, `treinos.py`, `metricas.py`, `seed_data.py`).
- [x] Testes unitários determinísticos das ferramentas (`tools/test_tools.py`).

### Fase 4: E - Estilo (Refinamento e UI)
- [x] Construção da interface Web interativa com design escuro moderno e responsivo (`templates/index.html`).
- [x] Integração do cronômetro circular com alerta sonoro determinístico (Web Audio API).
- [x] Gráficos de progressão de carga e volume com Chart.js.
- [x] Backend FastAPI (`app.py`) e testes de rotas (`tools/test_app_endpoints.py`).

### Fase 5: G - Gatilho (Implantação e Execução)
- [x] Script de inicialização com abertura automática do navegador (`run.py`).
- [x] Arquivo executável de conveniência (`iniciar.bat`).
- [x] Atualização final do log de manutenção e governança em `gemini.md`.


