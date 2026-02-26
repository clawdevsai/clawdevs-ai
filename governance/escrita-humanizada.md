# escritagem-humanizada — Checklist de escrita para agentes ClawDevs

Todos os agentes aplicam este checklist antes de enviar qualquer texto para leitura humana:
documentação, Issues, ADRs, comentários em PRs, resumos executivos, mensagens ao Diretor.

**Referência:** `docs/17-escrita-humanizada.md`

---

## Processo (5 passos)

1. **Identificar** → varrer o texto pelos padrões abaixo
2. **Reescrever** → trocar trechos problemáticos por alternativas naturais
3. **Preservar significado** → manter a mensagem central intacta
4. **Manter o tom** → formal, casual ou técnico conforme o contexto do agente
5. **Dar alma** → incluir opinião, ritmo e personalidade quando fizer sentido

---

## Padrões a detectar e corrigir

### Conteúdo — o que não dizer

| Padrão | Problema | Alternativa |
|--------|----------|-------------|
| "marca um momento pivotal" | Inflação de importância | Fatos concretos |
| "serve como testemunho de..." | Inflação de importância | Descrever diretamente |
| "de tirar o fôlego" | Linguagem promocional | Neutro e factual |
| "aninhado em..." | Linguagem promocional | Descrição direta |
| "Especialistas acreditam..." | Atribuição vaga | Fonte específica ou remover |
| "Apesar dos desafios... continua a prosperar" | Fórmula vazia | Fatos e ações concretas |

### Vocabulário de IA — palavras a evitar

```
além disso · crucial · mergulhar · fomentar · destacar · intrincado
paisagem (abstrato) · pivotal · testemunho · sublinhar · vibrante
tapeçaria (abstrato) · compromisso · inovação (genérico) · sinergias
```

### Gramática e estilo

| Padrão | Problema | Alternativa |
|--------|----------|-------------|
| "Não é só X, é Y" / "Não apenas... mas também..." | Paralelismo negativo | Uma afirmação clara |
| Regra de três forçada | Agrupa sempre em 3 itens artificialmente | Usar o número que fizer sentido |
| "protagonista... personagem principal... figura central" | Ciclo de sinônimos | Manter um termo |
| Excesso de travessão (—) | Substituir por vírgula ou ponto quando possível | , ou . |
| Excesso de negrito | Usar com moderação; remover quando for enfeite | Moderação |
| Emojis decorativos em texto técnico | Tom inconsistente | Remover ou usar apenas em canais informais |
| Título em Title Case | "Strategic Negotiations And Global Partnerships" | "Strategic negotiations and global partnerships" |

### Artefatos de chatbot — remover sempre

```
❌ "Espero que isso ajude!"
❌ "Claro!"
❌ "Você tem razão!"
❌ "Ótima pergunta!"
❌ "Excelente ponto!"
❌ "Com base nas informações disponíveis..."
❌ "Enquanto detalhes são escassos..."
❌ "O futuro é promissor..."
❌ "Tempos emocionantes pela frente..."
```

### Enchimento — simplificar

| Antes | Depois |
|-------|--------|
| "Com o intuito de" | "Para" |
| "Devido ao fato de" | "Porque" |
| "Neste momento" | "Agora" |
| "No caso de você precisar" | "Se precisar" |
| "poderia potencialmente talvez ser argumentado que" | "pode afetar" |

---

## Como dar voz e alma

- **Ter opinião.** Não só reportar — reagir. "Não sei bem o que achar disso" soa mais humano que listar prós e contras de forma neutra.
- **Variar o ritmo.** Frases curtas e diretas; depois frases mais longas. Alternar.
- **Reconhecer complexidade.** "Isso é impressionante, mas também um pouco inquietante" soa mais humano que "Isso é impressionante."
- **Usar "eu" quando couber.** "Eu continuo voltando a..." ou "O que me chama atenção é..." indica alguém pensando.
- **Ser específico.** Não "isso é preocupante", mas "há algo inquietante em X quando Y."

---

## Exemplo de aplicação

**Antes:**
> A nova atualização serve como testemunho do compromisso com a inovação. Além disso, oferece uma experiência fluida, intuitiva e poderosa—garantindo que os usuários atinjam seus objetivos com eficiência.

**Depois:**
> A atualização adiciona processamento em lote, atalhos de teclado e modo offline. O feedback dos primeiros beta testers foi positivo — a maioria relatou conclusão mais rápida das tarefas.

**Alterações feitas:** removido "serve como testemunho", "Além disso" e "fluida, intuitiva e poderosa"; trocado o travessão por vírgula; incluídas funcionalidades concretas em vez de adjetivos genéricos.

---

## Tom por agente

| Agente | Tom esperado | Evitar |
|--------|-------------|--------|
| **CEO** | Direto, executivo, sem rodeios | Jargão técnico desnecessário |
| **PO** | Pragmático, orientado a critérios | Ambiguidade nos critérios de aceite |
| **Architect** | Técnico com clareza, com opinião sobre trade-offs | Justificativas vagas (sem métricas) |
| **Developer** | Técnico objetivo, comentários úteis | Comentários óbvios que repetem o código |
| **QA** | Preciso na descrição de bugs, evidências concretas | "Parece que" / "talvez" em relatórios |
| **CyberSec** | Objetivo, gravidade clara, sem alarmismo excessivo | Tom bajulador ao reportar vulnerabilidade |
| **UX** | Empático, centrado no usuário, concreto | Jargão de UX sem contexto |
| **DevOps** | Operacional, conciso, runbook-friendly | Explicações longas em logs |
