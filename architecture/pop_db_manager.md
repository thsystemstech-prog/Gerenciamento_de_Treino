# POP 01 - Gerenciador de Banco de Dados SQLite (DB Manager)

## 1. Objetivo
Prover conexão determinística, inicialização de esquema relacional e operações de persistência local SQLite para o Gerenciador de Treinos.

## 2. Invariantes e Restrições
- O banco reside no caminho definido por `DATABASE_PATH` no `.env` (padrão: `data/treinos.db`).
- SQLite configurado com `PRAGMA foreign_keys = ON;` e `PRAGMA journal_mode = WAL;` para atomicidade e robustez.
- Todas as operações com dados utilizam consultas parametrizadas para evitar corrupção ou injeção.
- Não existem dependências externas de rede.

## 3. Modelo Relacional

### Tabela: `treinos_dia`
Representa a programação do treino para cada dia da semana.
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `dia_semana` TEXT NOT NULL UNIQUE (Valores: 'Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo')
- `tipo_treino` TEXT NOT NULL (Ex: 'Peito e Tríceps', 'Push', 'Pernas')
- `observacoes` TEXT
- `criado_em` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

### Tabela: `exercicios`
Exercícios atrelados ao treino do dia.
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `treino_dia_id` INTEGER NOT NULL REFERENCES treinos_dia(id) ON DELETE CASCADE
- `nome` TEXT NOT NULL
- `grupo_muscular` TEXT NOT NULL
- `ordem` INTEGER DEFAULT 1

### Tabela: `series_planejadas`
Configuração pré-definida de séries para cada exercício daquele dia.
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `exercicio_id` INTEGER NOT NULL REFERENCES exercicios(id) ON DELETE CASCADE
- `numero_serie` INTEGER NOT NULL
- `carga_kg` REAL NOT NULL DEFAULT 0.0
- `repeticoes` INTEGER NOT NULL DEFAULT 10
- `tecnica_avancada` TEXT NOT NULL DEFAULT 'Nenhuma'
- `tempo_descanso_segundos` INTEGER NOT NULL DEFAULT 60

### Tabela: `series_executadas`
Log real de execução de cada série (para alimentar métricas, histórico e evolução).
- `id` INTEGER PRIMARY KEY AUTOINCREMENT
- `exercicio_id` INTEGER NOT NULL REFERENCES exercicios(id) ON DELETE CASCADE
- `numero_serie` INTEGER NOT NULL
- `carga_kg` REAL NOT NULL
- `repeticoes` INTEGER NOT NULL
- `tecnica_avancada` TEXT NOT NULL DEFAULT 'Nenhuma'
- `tempo_descanso_segundos` INTEGER NOT NULL
- `concluido` INTEGER NOT NULL DEFAULT 1
- `executado_em` TIMESTAMP DEFAULT CURRENT_TIMESTAMP

## 4. Casos de Borda e Tratamento de Erros
1. **Diretório inexistente:** O módulo cria recursivamente a pasta `data/` antes de abrir a conexão.
2. **Dia da semana inválido:** Validado estritamente contra a lista dos 7 dias permitidos.
3. **Exclusão em cascata:** A exclusão de um treino do dia remove automaticamente exercícios e séries associadas.

