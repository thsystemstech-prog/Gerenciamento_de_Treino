# POP 03 - Cálculo de Métricas e Progressão de Carga

## 1. Objetivo
Processar dados históricos de `series_executadas` para fornecer relatórios determinísticos e séries temporais de evolução de carga, volume e repetições.

## 2. Fórmulas Matemáticas Determinísticas
- **Volume da Série ($V_s$):**
  $$V_s = \text{carga\_kg} \times \text{repeticoes}$$
- **Volume Total por Sessão/Exercício ($V_{\text{total}}$):**
  $$V_{\text{total}} = \sum V_s$$
- **Carga Máxima do Dia ($C_{\max}$):**
  $$C_{\max} = \max(\text{carga\_kg})$$
- **Estimativa de 1RM (Fórmula de Epley):**
  $$1RM = \text{carga\_kg} \times \left(1 + \frac{\text{repeticoes}}{30}\right)$$

## 3. Estrutura de Retorno para Gráficos
Retorna lista ordenada cronologicamente por exercício:
```json
[
  {
    "exercicio": "Supino Reto",
    "data": "2026-11-02",
    "carga_max_kg": 80.0,
    "volume_total_kg": 2400.0,
    "repeticoes_totais": 30,
    "um_rm_estimado": 106.67
  }
]
```

## 4. Casos de Borda
- Exercício sem execuções registradas: Retorna array vazio `[]` sem erro de execução.
- Séries com carga 0.0 (exercícios com peso do corpo): Calcula repetições totais e volume baseado em 0 kg.

