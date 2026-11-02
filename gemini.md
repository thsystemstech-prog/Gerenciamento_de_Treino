# gemini.md - Constituição do Projeto: Gerenciador de Treino

> Este arquivo é a lei e constituição do projeto. Nenhuma lógica em `tools/` pode desviar das regras e esquemas aqui definidos.

---

## 1. Visão Geral
- **Nome do Projeto:** Gerenciador de Treino
- **Metodologia:** Protocolo V.L.A.E.G. (Visão, Link, Arquitetura, Estilo, Gatilho) & Arquitetura A.N.T. em 3 Camadas
- **Status:** Fase 1 - Descoberta e Definição de Visão

---

## 2. Invariantes Arquiteturais
1. **Separação em 3 Camadas:**
   - **Camada 1 (Arquitetura):** POPs técnicos em `architecture/*.md`.
   - **Camada 2 (Navegação):** Piloto/Agente raciocina e orquestra a chamada de ferramentas determinísticas.
   - **Camada 3 (Ferramentas):** Scripts Python atômicos, testáveis e determinísticos em `tools/`.
2. **Arquivos Temporários:** Todas as etapas intermediárias de leitura/escrita de arquivos locais devem usar exclusivamente a pasta `.tmp/`.
3. **Segredos e Credenciais:** Nunca expor segredos no código; utilizar sempre `.env`.
4. **Atualização Prévia de POP:** Se a lógica de execução mudar, atualize o POP correspondente antes de alterar o código.

---

## 3. Regras Comportamentais
- Não adivinhar regras de negócio; esclarecer sempre com o usuário.
- Confiabilidade e determinismo sobre velocidade.
- Seguir o loop de autocorreção em caso de falhas (Analisar -> Corrigir -> Testar -> Atualizar Arquitetura).

---

## 4. Esquema de Dados (Data Schemas)

### Input Schema (Dados Brutos de Entrada / Cadastro e Registro)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RegistroTreinoInput",
  "type": "object",
  "required": ["dia_semana", "tipo_treino", "exercicios"],
  "properties": {
    "dia_semana": {
      "type": "string",
      "enum": ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
    },
    "tipo_treino": {
      "type": "string",
      "description": "Ex: Hipertrofia, Força, Push, Pull, Pernas, Superior, etc."
    },
    "observacoes": {
      "type": "string"
    },
    "exercicios": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["nome", "series"],
        "properties": {
          "nome": { "type": "string" },
          "grupo_muscular": { "type": "string" },
          "series": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["numero_serie", "carga_kg", "repeticoes", "tempo_descanso_segundos"],
              "properties": {
                "numero_serie": { "type": "integer", "minimum": 1 },
                "carga_kg": { "type": "number", "minimum": 0 },
                "repeticoes": { "type": "integer", "minimum": 1 },
                "tecnica_avancada": {
                  "type": "string",
                  "enum": ["Nenhuma", "Drop-set", "Rest-pause", "Bi-set", "Tri-set", "Super-slow", "Pirâmide Crescente", "Pirâmide Decrescente", "Cluster Sets", "Pausa Isométrica"]
                },
                "tempo_descanso_segundos": { "type": "integer", "minimum": 0, "description": "Tempo de intervalo entre séries em segundos" }
              }
            }
          }
        }
      }
    }
  }
}
```

### Output Schema (Payload de Entrega / Consulta e Visualização)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TreinoPayloadOutput",
  "type": "object",
  "required": ["status", "dia_selecionado", "treino_dia", "historico_progressao"],
  "properties": {
    "status": {
      "type": "string",
      "enum": ["sucesso", "erro", "vazio"]
    },
    "mensagem": {
      "type": "string"
    },
    "dia_selecionado": {
      "type": "string"
    },
    "treino_dia": {
      "type": "object",
      "properties": {
        "id": { "type": "integer" },
        "dia_semana": { "type": "string" },
        "tipo_treino": { "type": "string" },
        "total_exercicios": { "type": "integer" },
        "total_series": { "type": "integer" },
        "tempo_total_estimado_min": { "type": "number" },
        "exercicios": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "exercicio_id": { "type": "integer" },
              "nome": { "type": "string" },
              "grupo_muscular": { "type": "string" },
              "series": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "serie_id": { "type": "integer" },
                    "numero_serie": { "type": "integer" },
                    "carga_kg": { "type": "number" },
                    "repeticoes": { "type": "integer" },
                    "tecnica_avancada": { "type": "string" },
                    "tempo_descanso_segundos": { "type": "integer" },
                    "concluido": { "type": "boolean" },
                    "data_hora_execucao": { "type": "string" }
                  }
                }
              }
            }
          }
        }
      }
    },
    "historico_progressao": {
      "type": "array",
      "description": "Dados para alimentação de gráficos de evolução de carga e volume por exercício",
      "items": {
        "type": "object",
        "properties": {
          "exercicio": { "type": "string" },
          "data": { "type": "string" },
          "carga_max_kg": { "type": "number" },
          "volume_total_kg": { "type": "number" },
          "repeticoes_totais": { "type": "integer" }
        }
      }
    }
  }
}
```

---

## 5. Log de Manutenção
- **2026-11-02:** Protocolo 0 executado. Estrutura base e constituição criadas.
- **2026-11-02:** Fase 1 (Visão) concluída. Data Schemas definidos e Blueprint aprovado.
- **2026-11-02:** Fase 2 (Link) concluída. Handshake testado e validado em `tools/test_link.py`.
- **2026-11-02:** Fase 3 (Arquitetura) concluída. Criados 4 POPs em `architecture/` e ferramentas em `tools/` (`db.py`, `treinos.py`, `metricas.py`, `seed_data.py`). Testes unitários passaram 100%.
- **2026-11-02:** Fase 4 (Estilo) concluída. Construção da interface Web SPA interativa em FastAPI/HTML5/CSS3 com Cronômetro sonoro e Gráficos de evolução (Chart.js).
- **2026-11-02:** Fase 5 (Gatilho) concluída. Criados executáveis locais `run.py` e `iniciar.bat`. Sistema pronto para uso.

