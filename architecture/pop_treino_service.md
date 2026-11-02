# POP 02 - Serviço de Treinos e Séries (Treino Service)

## 1. Objetivo
Definir as operações de negócio determinísticas para gerenciar o planejamento semanal, consulta diária e registro de execuções de séries.

## 2. Entradas e Validações
- **Dia da Semana:** Deve pertencer ao conjunto fixo: `['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']`.
- **Carga:** Valor decimal `>= 0.0`.
- **Repetições:** Inteiro positivo `>= 1`.
- **Tempo de Descanso:** Inteiro `>= 0` (em segundos). Padrão: 60s.
- **Técnicas Avançadas Suportadas:**
  - `Nenhuma`
  - `Drop-set`
  - `Rest-pause`
  - `Bi-set`
  - `Tri-set`
  - `Super-slow`
  - `Pirâmide Crescente`
  - `Pirâmide Decrescente`
  - `Cluster Sets`
  - `Pausa Isométrica`

## 3. Fluxo de Operações Determinísticas

### Operação A: `salvar_ou_atualizar_treino_dia`
1. Abre transação no SQLite.
2. Faz upsert em `treinos_dia` com base em `dia_semana`.
3. Se existirem exercícios anteriores no plano daquele dia, remove ou substitui de acordo com a lista enviada.
4. Insere cada exercício e suas respectivas `series_planejadas`.
5. Confirma transação (`COMMIT`). Em caso de erro, executa `ROLLBACK`.

### Operação B: `obter_resumo_semanal`
1. Consulta todos os 7 dias da semana.
2. Para cada dia, retorna `tipo_treino`, quantidade de exercícios e quantidade total de séries cadastradas.
3. Se um dia não possuir cadastro, retorna status "Descanso / Vazio".

### Operação C: `obter_treino_detalhado(dia_semana)`
1. Busca treino correspondente ao dia.
2. Carrega lista de exercícios ordenados.
3. Para cada exercício, carrega as séries planejadas e as últimas séries executadas na data atual.

### Operação D: `registrar_execucao_serie`
1. Grava uma nova linha em `series_executadas` com timestamp atual.
2. Retorna confirmação e tempo de descanso recomendado para acionamento do cronômetro.

## 4. Casos de Borda
- Inserir séries com valores negativos: Bloqueado por validação.
- Registrar execução de exercício sem treino ativo: Requer exercício válido pré-cadastrado.

