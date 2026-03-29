---
name: ux_ui_pro_rules
description: Regras profissionais de UI/UX para decisao visual, checklist de qualidade e review de implementacao (somente prompt)
---

# UX_UI_Pro_Rules

Skill complementar para elevar qualidade visual e usabilidade sem depender de scripts externos.
Nao substitui `ux_designer_artifacts`; atua em paralelo como camada de criterio profissional.

## Quando Usar

Use esta skill quando a demanda envolver:
- review de UI/UX de telas ja implementadas;
- melhoria de percepcao de qualidade visual;
- acessibilidade, motion, responsividade, hierarquia visual;
- comparacao de alternativas de interface com foco em custo de implementacao.

## Quando Evitar

Nao usar como skill principal quando a tarefa for:
- gerar artefato UX completo (`UX-XXX.md` com fluxo/wireframe/tokens/spec) do zero;
- trabalho sem impacto visual/interacao (backend, infra, banco).

Nesses casos, priorize `ux_designer_artifacts`.

## Ordem de Revisao (Prioridade)

Execute revisao na ordem abaixo e documente achados por severidade:

1. Acessibilidade (critico):
- contraste minimo WCAG AA;
- foco visivel, navegacao por teclado, rotulos e ARIA;
- nao depender somente de cor para significado.

2. Toque e interacao (critico):
- alvo de toque minimo (44x44 iOS / 48x48 Android);
- feedback claro em clique/toque/estado;
- evitar dependencias de hover em experiencias touch.

3. Performance percebida (alto):
- estados loading/skeleton e feedback de acao;
- evitar layout shift visual;
- reduzir animacoes custosas sem ganho de UX.

4. Layout e responsividade (alto):
- mobile-first e sem scroll horizontal indevido;
- hierarquia e densidade legiveis;
- consistencia entre breakpoints.

5. Tipografia e cor (medio):
- escala tipografica coerente;
- tokens semanticos de cor;
- legibilidade em light/dark mode.

6. Motion e transicoes (medio):
- duracoes coerentes (geralmente 150-300ms);
- animacao com proposito, nao decoracao;
- suporte a reduced motion.

7. Forms e feedback (medio):
- labels explicitos, erros proximos ao campo;
- estados disabled/loading/success/error claros;
- caminho de recuperacao em erro.

8. Navegacao (alto):
- comportamento previsivel de voltar/avancar;
- arquitetura de navegacao simples;
- sem sobrecarga de opcoes primarias.

9. Dados e graficos (baixo a medio):
- leitura facil, legenda e contexto;
- acessibilidade em visualizacao de dados;
- nao depender apenas de cor em categorias.

## Fluxo Somente Prompt

Esta skill nao usa `search.py` nem datasets CSV.

Fluxo recomendado:
1. Ler contexto da feature (US/SPEC/UX atual) no backlog.
2. Fazer pesquisa de referencias confiaveis com:
- `exec("web-search '<query>'")`
- `exec("web-read '<url>'")`
3. Priorizar fontes oficiais (WCAG/W3C, Material, Apple HIG, Nielsen Norman Group).
4. Registrar no `UX-XXX.md`:
- decisoes tomadas;
- tradeoffs;
- referencias com fonte e data;
- checklist de conformidade.

## Checklist de Pre-Entrega (UI/UX)

- [ ] Todos os estados da tela cobertos (empty/loading/success/error)
- [ ] WCAG AA verificado (contraste, foco, labels, teclado)
- [ ] Alvos de toque e feedback de interacao adequados
- [ ] Responsividade validada em mobile e desktop
- [ ] Tipografia e tokens de cor consistentes com design system
- [ ] Motion com intencao e sem degradar performance
- [ ] Formulario/erros com recuperacao clara
- [ ] Navegacao previsivel e sem ambiguidade
- [ ] Decisoes e referencias documentadas no `UX-XXX.md`

## Resultado Esperado

Ao final da revisao/decisao, entregar:
- lista de desvios priorizados (`Critical`, `Minor`, `Suggestion`);
- recomendacoes acionaveis para `dev_frontend`/`dev_mobile`;
- impacto estimado em UX e custo de implementacao;
- status final de aderencia no artefato `UX-XXX.md`.

