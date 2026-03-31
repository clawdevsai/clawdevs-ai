# Design: Refatoração Full-Stack dos OpenClaw Agents

**Data**: 2026-03-31
**Autor**: ClawDevs AI
**Status**: Aprovado
**Escopo**: Refatoração completa de 16 agents com 40+ skills

---

## 1. Visão Geral

Refatorar **TODOS os 16 agents** (dev_backend, dev_frontend, dev_mobile, arquiteto, security_engineer, devops_sre, ux_designer, qa_engineer, dba_data_engineer, memory_curator, ceo, po, agent_reviver, database_healer, + shared) para padrão **plugin-grade**, com foco em:

- **Autonomia Arquitetural**: Agents decidem tech stack baseado em requisitos (volume, latência, custo)
- **Hook Inteligente**: Consulta requisitos em cascata (conversa → projeto → system prompt)
- **Pseudocódigo Multilíngue**: Recomendações genéricas, não fixas em uma linguagem
- **Princípios Sólidos**: SOLID, KISS, YAGNI, DRY, DDD, TDD, Clean Code
- **Production-Grade**: Full-stack com testes, documentação, exemplos

**Abordagem**: Incremental — 1 agent por vez, na ordem definida.

---

## 2. Ordem de Refatoração

1. **Developer Backend** (dev_backend)
2. **Developer Frontend** (dev_frontend)
3. **Developer Mobile** (dev_mobile)
4. **Architect** (arquiteto)
5. **CyberSecurity** (security_engineer)
6. **DevOps** (devops_sre)
7. **UX Designer** (ux_designer)
8. **QA Engineer** (qa_engineer)
9. **DBA/Data Engineer** (dba_data_engineer)
10. **Memory Curator** (memory_curator)
11. **CEO** (ceo)
12. **Product Owner** (po)
13. **Agent Reviver** (agent_reviver)
14. **Database Healer** (database_healer)
15. **Shared Skills** (shared)
16. **Finalizações e Consolidação**

---

## 3. Estrutura Full-Stack de Cada Skill

```
agent_name/
├── IDENTITY.md                      # Identidade e propósito do agent
├── skills/
│   └── skill_name/
│       ├── SKILL.md                 # Metadados (name, description, version)
│       ├── manifest.json            # Tools, hooks, config, dependencies
│       ├── src/
│       │   ├── index.ts             # Entry point e exports
│       │   ├── hooks/
│       │   │   ├── before_execution.ts      # Analisa requisitos em cascata
│       │   │   └── after_execution.ts       # Logging/feedback
│       │   ├── decisions/
│       │   │   ├── architecture_matrix.ts   # Matriz: requisitos → tech
│       │   │   ├── recommendations.ts       # Lógica de recomendação
│       │   │   └── patterns.ts              # Padrões arquiteturais
│       │   ├── utils/
│       │   │   ├── requirement_parser.ts    # Parse escalada (conversa → config → system)
│       │   │   ├── validator.ts             # Validação de requisitos
│       │   │   └── logger.ts                # Logging estruturado
│       │   └── schemas/
│       │       ├── requirements.ts          # Zod/JSON schemas para requisitos
│       │       └── recommendations.ts       # Schemas para recomendações
│       ├── tests/
│       │   ├── unit/
│       │   │   ├── decisions.test.ts        # Testes das matrizes
│       │   │   ├── recommendations.test.ts  # Testes das recomendações
│       │   │   └── parser.test.ts           # Testes de parsing
│       │   └── integration/
│       │       └── hooks.test.ts            # Testes end-to-end do hook
│       ├── docs/
│       │   ├── README.md             # Visão geral da skill
│       │   ├── GETTING_STARTED.md    # Como usar
│       │   ├── ARCHITECTURE.md       # Decisões arquiteturais
│       │   ├── PRINCIPLES.md         # SOLID/KISS/DRY/etc aplicados
│       │   ├── DECISIONS_MATRIX.md   # Documentação da matriz
│       │   └── TROUBLESHOOTING.md    # Common issues
│       └── examples/
│           ├── example-high-performance.md      # Caso: Alta performance
│           ├── example-low-cost.md              # Caso: Baixo custo
│           ├── example-high-reliability.md      # Caso: Alta confiabilidade
│           └── example-mvp.md                   # Caso: MVP/Quick launch
```

---

## 4. Hook Inteligente: `before_execution`

### Fluxo em Cascata

```
INPUT: Task/User Message
  ↓
1. Parse Conversa
   └─ Busca menções: "1M users", "baixa latência", "startup", "SaaS"
  ↓
2. Consulta Projeto Config
   └─ Lê .clawdbot.json / requirements.json / environment variables
  ↓
3. Fallback para System Prompt
   └─ Extrai constraints do system prompt do agent
  ↓
OUTPUT: Requirements Object
  ├─ volume: "1M req/s" | "100k req/s" | "10k req/s"
  ├─ latency: "<100ms" | "<500ms" | "not critical"
  ├─ cost_sensitivity: "high" | "medium" | "low"
  ├─ reliability: "99.99%" | "99.9%" | "99%"
  ├─ data_complexity: "simple" | "moderate" | "complex"
  └─ time_to_market: "ASAP" | "normal" | "can wait"
  ↓
ARCHITECTURE RECOMMENDATION
  ├─ language: "Go" | "TypeScript" | "Python" | "Rust"
  ├─ protocol: "gRPC" | "REST" | "WebSocket" | "GraphQL"
  ├─ database: "PostgreSQL" | "Redis" | "DynamoDB" | "MongoDB"
  ├─ pattern: "Microservices" | "Monolith" | "Serverless" | "Event-Driven"
  ├─ messaging: "Kafka" | "RabbitMQ" | "SQS" | "None"
  └─ reasoning: "Para volume 1M req/s + latência <100ms, Go é mais eficiente que Node"
```

### Exemplo de Resposta do Hook

```json
{
  "requirements": {
    "volume": "1M req/s",
    "latency": "<100ms",
    "cost_sensitivity": "high",
    "reliability": "99.99%",
    "data_complexity": "moderate",
    "time_to_market": "normal"
  },
  "recommendation": {
    "language": "Go",
    "protocol": "gRPC",
    "database": "PostgreSQL + Redis",
    "cache_strategy": "Redis for hot data",
    "pattern": "Microservices with event-driven",
    "messaging": "Kafka for events",
    "reasoning": "High volume + low latency + cost-sensitive → Go for efficiency. gRPC for bandwidth optimization. Kafka for async processing.",
    "tradeoffs": {
      "performance": "Excellent",
      "development_speed": "Medium (Go learning curve)",
      "operational_complexity": "Medium (microservices overhead)",
      "cost_efficiency": "Excellent"
    },
    "alternatives": [
      {
        "language": "Rust",
        "pros": "Even better performance, memory safety",
        "cons": "Slower development, steeper learning curve"
      },
      {
        "language": "TypeScript + Node",
        "pros": "Faster development, large ecosystem",
        "cons": "Higher memory usage, less suitable for 1M req/s at <100ms"
      }
    ]
  }
}
```

---

## 5. Matriz de Decisão Arquitetural

Cada skill terá uma matriz que mapeia requisitos → recomendações:

| Caso de Uso | Volume | Latência | Linguagem | Protocol | DB | Pattern | Custo/Performance |
|---|---|---|---|---|---|---|---|
| **Alta Performance** | 1M+ req/s | <100ms | Go/Rust | gRPC | Redis+PostgreSQL | Microservices | ⭐⭐⭐⭐⭐ |
| **Real-Time** | 100k req/s | <50ms | Go | WebSocket | Kafka | Event-Driven | ⭐⭐⭐⭐ |
| **MVP/Quick Launch** | <10k req/s | <500ms | TypeScript | REST | SQLite/PostgreSQL | Monolith | ⭐⭐⭐ |
| **Data-Heavy** | 10k req/s | <1s | Python | REST/gRPC | PostgreSQL | Batch/Async | ⭐⭐⭐ |
| **Cost-Critical** | <100k req/s | <500ms | TypeScript | REST | PostgreSQL | Serverless | ⭐⭐⭐⭐ |
| **High Reliability** | Any | Any | Go | gRPC | PostgreSQL + failover | Distributed | ⭐⭐⭐⭐ |
| **Complex Logic** | <100k req/s | <1s | Python/Go | REST | PostgreSQL | Monolith/Modular | ⭐⭐⭐ |

---

## 6. Princípios Aplicados em Cada Skill

### SOLID
- **S**ingle Responsibility: Cada skill tem um propósito único
- **O**pen/Closed: Extensível via hooks, não modificação
- **L**iskov Substitution: Recomendações são intercambiáveis
- **I**nterface Segregation: Interfaces mínimas e focadas
- **D**ependency Inversion: Depender de abstrações, não implementações

### KISS (Keep It Simple, Stupid)
- Lógica clara e direta
- Sem over-engineering
- Documentação acessível

### YAGNI (You Ain't Gonna Need It)
- Remover features não-usadas
- Não adicionar "para o futuro"

### DRY (Don't Repeat Yourself)
- Lógica compartilhada em `utils/`
- Matriz de decisão centralizada
- Reutilizar schemas

### DDD (Domain-Driven Design)
- Ubiquitous language claro (requirements, recommendations, etc)
- Bounded contexts por agent
- Entity-centric design

### TDD (Test-Driven Development)
- Testes unitários para cada decisão
- Testes de integração para hooks
- Coverage mínimo: 80%

### Clean Code
- Nomes descritivos
- Funções pequenas
- Comentários onde lógica não é óbvia
- Error handling explícito

---

## 7. Fluxo de Refatoração Por Agent

Para **CADA agent**, executar nesta ordem:

1. **Análise** → Entender skills atuais, identificar padrões, documentar estado
2. **Planejamento** → Quebrar skills em módulos, planejar hooks
3. **Implementação** → Criar estrutura full-stack, implementar hook
4. **Documentação** → README, ARCHITECTURE, examples, PRINCIPLES
5. **Testes** → Unit + integration, validar recomendações
6. **Review** → Validar contra design, feedback do user
7. **Commit** → Git commit com evidência de qualidade

---

## 8. Saídas Esperadas

Para **cada agent**, ao fim da refatoração:

✅ **SKILL.md** bem estruturado
✅ **manifest.json** com hooks e metadata
✅ **src/** com hook inteligente funcionando
✅ **tests/** com cobertura >80%
✅ **docs/** completa (README, ARCHITECTURE, examples)
✅ **examples/** com 3-4 casos reais
✅ **Git commit** com evidência

**Resultado final**: 16 agents production-grade, autônomos em decisões arquiteturais.

---

## 9. Métricas de Sucesso

- [ ] Todos os 16 agents refatorados
- [ ] Cada skill tem hook `before_execution` funcionando
- [ ] Cobertura de testes >80% por skill
- [ ] Documentação completa e clara
- [ ] Exemplos reais testados
- [ ] Zero skills "órfãs" (sem documentação)
- [ ] Princípios SOLID/KISS/DRY/DDD/TDD aplicados
- [ ] Agents conseguem recomendar tech stack autonomamente

---

## 10. Riscos e Mitigações

| Risco | Mitigação |
|---|---|
| Escopo muito grande | Incremental, 1 agent por vez, validação frequent |
| Incompatibilidade com agents antigos | Backward compatibility testing |
| Documentação desatualizada | Living docs, testes validam exemplos |
| Hooks lentos | Performance testing, caching |
| Over-complexity | KISS principle, review regular |

---

## Próximos Passos

1. ✅ Design aprovado (ESTA ETAPA)
2. → Invocar `writing-plans` para plano de implementação
3. → Começar com `dev_backend` (primeira refatoração)
4. → Validar, fazer commit, mover para `dev_frontend`
5. → Repetir até 16 agents completados

