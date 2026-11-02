# Descobertas e Restrições (Findings) - Gerenciador de Treino

## Pesquisas e Descobertas
- Projeto inicializado seguindo a metodologia **Protocolo V.L.A.E.G.** e arquitetura em 3 camadas A.N.T.
- Documento de referência do protocolo localizado em `Passo a Passo/protocolo_vlaeg.md`.

### Visão e Funcionalidades Coletadas (Fase 1)
- **Objetivo Central:** Aplicativo web de gerenciamento de treinos semanal com acompanhamento dia a dia.
- **Entidades e Campos Confirmados:**
  - Planejamento semanal (Segunda a Domingo).
  - Tipo de treino (Hipertrofia, Força, Push, Pull, Legs, etc.).
  - Exercícios agrupados por treino/grupo muscular.
  - Carga (kg), Repetições, Técnicas Avançadas (Drop-set, Rest-pause, etc.).
  - Tempo de descanso e intervalo entre séries (segundos).
- **Recursos Comportamentais Específicos:**
  - Cronômetro/Timer interativo com aviso sonoro para descanso entre séries.
  - Histórico e gráficos de progressão de carga por exercício ao longo do tempo.
- **Decisões de Stack e Arquitetura:**
  - **Interface:** Aplicação Web interativa em Python (Streamlit com layout limpo e moderno ou FastAPI com front HTML5/JS responsivo).
  - **Fonte da Verdade:** SQLite local (`data/treinos.db`).
  - **Conectividade:** 100% offline e local (sem necessidade de chaves de API pagas ou serviços de nuvem).

## Restrições e Invariantes
- **Regra de Ouro:** Não escrever scripts em `tools/` antes das Perguntas de Descoberta respondidas, esquemas definidos em `gemini.md` e blueprint aprovado em `task_plan.md`.
- Arquitetura de 3 camadas: POPs (`architecture/`), Decisão/Navegação (Piloto/LLM), Execução (`tools/`).
- Operações intermediárias restritas a `.tmp/`.
- **Aprendizado de Ambiente Windows (Encoding):** O console do Windows opera nativamente com CP1252. Em scripts Python CLI e logs, sempre garantir `sys.stdout.reconfigure(encoding='utf-8')` ou saída ASCII segura para evitar `UnicodeEncodeError`.




