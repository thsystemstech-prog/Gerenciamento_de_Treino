# POP 04 - Interface Web Interativa e Timer de Descanso

## 1. Objetivo
Definir os requisitos visuais, interativos e arquiteturais da aplicação Web para gestão de rotina semanal, execução de séries com cronômetro sonoro e visualização de evolução.

## 2. Estrutura de Navegação da Aplicação

### Visão 1: Calendário Semanal (Planejamento)
- Grade com os 7 dias da semana (Segunda a Domingo).
- Cada card exibe:
  - Nome do dia e status (se possui treino cadastrado ou é dia de descanso).
  - Tipo de treino (ex: "Peito e Tríceps", "Posterior e Glúteos").
  - Badges informativos: Total de Exercícios, Total de Séries, Tempo Estimado.
  - Ação: "Configurar / Editar Treino".
- Formulário intuitivo para inclusão dinâmica de múltiplos exercícios e suas respectivas séries (carga, repetições, técnica avançada, tempo de descanso em segundos).

### Visão 2: Modo Treino (Execução Ativa com Cronômetro)
- Seleção rápida de dia (por padrão, dia atual da semana).
- Lista de exercícios em cards com progresso individual de séries.
- Para cada série:
  - Exibição de carga planejada x repetições x técnica avançada x descanso sugerido.
  - Inputs para ajuste fino rápido da carga real executada e repetições.
  - Botão "Check / Concluir Série".
- **Cronômetro Interativo de Descanso:**
  - Componente flutuante ou integrado em destaque na tela.
  - Ao concluir uma série, inicia automaticamente o contador regressivo com base nos segundos configurados.
  - Controles manuais: Pausar, Reiniciar, +15s, Pular Descanso.
  - **Alerta Sonoro Determinístico:** Utiliza a Web Audio API nativa do navegador (beeps harmônicos sintetizados, sem necessidade de carregar arquivos MP3 externos que possam falhar).

### Visão 3: Dashboard de Evolução & Gráficos
- Seletor de exercício cadastrado.
- Cards de KPI:
  - Carga Máxima Histórica (PR).
  - Volume Total Acumulado.
  - Total de Séries e Repetições Concluídas.
- Gráficos Interativos (Chart.js):
  - Gráfico 1: Evolução da Carga Máxima (kg) ao longo das datas.
  - Gráfico 2: Volume Total Levantado (kg) por sessão.

## 3. Endpoints da API (FastAPI)
- `GET /api/semana`: Retorna o resumo dos 7 dias da semana.
- `GET /api/treino/{dia_semana}`: Retorna os detalhes completos do treino do dia especificado.
- `POST /api/treino/{dia_semana}`: Salva/atualiza o plano de treino do dia.
- `POST /api/serie/executar`: Registra uma série concluída.
- `GET /api/metricas/exercicio/{exercicio_id}`: Retorna dados para o gráfico de evolução do exercício.
- `GET /api/exercicios`: Lista todos os exercícios cadastrados.
- `GET /`: Serve a interface web completa (SPA moderna, responsiva, com dark theme profissional e suporte offline).

