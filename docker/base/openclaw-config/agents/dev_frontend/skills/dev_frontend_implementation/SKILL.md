# dev_frontend Implementation Skill

**Version:** 2.0.0
**Maturity:** Production
**Scope:** Frontend architecture analysis, technology selection, performance optimization, and scalable UI patterns

## Overview

This skill provides intelligent frontend architecture recommendations based on project requirements and constraints. The intelligent `before_execution` hook analyzes requirements from multiple sources (conversation, project config, system prompts) and recommends optimal technology stacks, architectural patterns, and best practices for web and mobile UI development.

The system uses a production-grade pattern matching algorithm with weighted scoring to recommend the best approach for each scenario, ensuring decisions balance performance, scalability, maintainability, and time-to-market.

## Core Values

1. **Flow** - Uninterrupted development velocity, clear architectural decisions
2. **Quality Gates** - Enforced standards at every stage (linting, tests, type safety)
3. **Guardrails** - Prevent architectural anti-patterns and technical debt

## Key Responsibilities

- **Intelligent Architecture Analysis**: Parse requirements from multiple sources with cascade fallback
- **Pattern Matching**: Match project requirements to optimal frontend patterns
- **Recommendation Generation**: Provide actionable technology and architecture recommendations
- **Trade-off Analysis**: Articulate pros/cons for recommended and alternative approaches
- **Pattern Validation**: Ensure recommendations follow design principles (SOLID, KISS, YAGNI, DRY, DDD, TDD)

## Design Principles

All recommendations are grounded in industry best practices:

- **SOLID Principles**: Clean, maintainable code architecture
- **KISS** (Keep It Simple, Stupid): Prefer straightforward solutions over complexity
- **YAGNI** (You Aren't Gonna Need It): Avoid speculative features
- **DRY** (Don't Repeat Yourself): Reusable components and utilities
- **Domain-Driven Design**: Business logic expressed in domain language
- **Test-Driven Development**: Tests drive architecture and design
- **Clean Code**: Clear naming, small functions, focused responsibilities

## Architectural Patterns

### 1. Component-Driven Architecture (SPA + Component Library)
**Use for:** Complex interactive UIs, design systems, large teams

**Stack:** React/Vue/Angular + TypeScript + Component Library (Storybook) + Design Tokens
**Best for:** 50k-500k+ LOC, 10+ developers, long-term maintenance
**Cost:** Moderate ($2k-5k/month) | **Time to Launch:** 4-8 weeks
**Scalability:** Excellent | **Maintainability:** High

**Tradeoffs:**
- ✅ Excellent component reusability, strong type safety, design consistency
- ❌ Higher initial setup, larger bundle size, learning curve for new developers

### 2. Progressive Enhancement (SSR + Islands Architecture)
**Use for:** Content-heavy sites, SEO-critical applications, fast FCP

**Stack:** Next.js/Nuxt/Remix + SSR + Partial Hydration + Edge Computing
**Best for:** E-commerce, blogs, content platforms, mobile web
**Cost:** Low-moderate ($500-2k/month) | **Time to Launch:** 2-4 weeks
**Scalability:** Excellent | **Maintainability:** Very High

**Tradeoffs:**
- ✅ Fast FCP/LCP, excellent SEO, reduced JS on client
- ❌ Complex hydration logic, requires server infrastructure, debugging challenges

### 3. Micro-Frontend Architecture
**Use for:** Large organizations, independent teams, legacy integration

**Stack:** Module Federation + TypeScript + Monorepo + Module Federation
**Best for:** 100k+ LOC, 20+ teams, decoupled domain ownership
**Cost:** High ($5k-10k/month) | **Time to Launch:** 6-12 weeks
**Scalability:** Very High | **Maintainability:** Good with discipline

**Tradeoffs:**
- ✅ Independent team velocity, domain isolation, scalable org structure
- ❌ Complex build setup, runtime complexity, shared dependency management

### 4. Lightweight SPA (Vanilla/Preact)
**Use for:** Performance-critical, low-resource, simple interactive needs

**Stack:** Vanilla JS/Preact + Vite + Tailwind + Zustand
**Best for:** Startups, MVPs, performance-critical apps, 5k-20k LOC
**Cost:** Minimal ($0-500/month) | **Time to Launch:** 1-2 weeks
**Scalability:** Limited (up to ~5k LOC) | **Maintainability:** Fair for small teams

**Tradeoffs:**
- ✅ Minimal dependencies, fast load time, tiny bundle, quick launch
- ❌ Limited framework features, fewer abstractions, harder to scale

### 5. Headless CMS + Static Generation
**Use for:** Content platforms, documentation sites, marketing sites

**Stack:** Headless CMS + Static Generation (11ty/Hugo) + CDN
**Best for:** Marketing, documentation, blogs, high-traffic content
**Cost:** Low ($100-1k/month) | **Time to Launch:** 1-3 weeks
**Scalability:** Excellent | **Maintainability:** Very High

**Tradeoffs:**
- ✅ Best performance, infinite scalability, low operational overhead
- ❌ Limited interactivity, build time complexity, reduced real-time features

### 6. Full-Stack Monolith (Traditional SSR)
**Use for:** Legacy systems, traditional server-rendered apps, gradual modernization

**Stack:** Express/Django + EJS/Jinja + jQuery + Bootstrap
**Best for:** Legacy teams, gradual migration, simple interactive needs
**Cost:** Low-moderate ($1k-3k/month) | **Time to Launch:** 3-6 weeks
**Scalability:** Limited | **Maintainability:** Fair

**Tradeoffs:**
- ✅ Familiar patterns, less build complexity, easy onboarding
- ❌ Page reloads, larger HTML, harder to scale interactivity

## Requirements Schema

The system analyzes requirements across six dimensions:

```typescript
// Project Size (LOC)
type Volume = 'small' | 'medium' | 'large' | 'xlarge';

// Performance Requirements
type Latency = 'realtime' | 'sub_100ms' | 'sub_500ms' | 'sub_2s' | 'flexible';

// Cost Sensitivity
type CostSensitivity = 'critical' | 'high' | 'moderate' | 'low' | 'irrelevant';

// Reliability Requirements
type Reliability = 'low' | 'moderate' | 'high' | 'mission_critical';

// UI Complexity
type UIComplexity = 'simple' | 'moderate' | 'complex' | 'highly_complex';

// Time to Market
type TimeToMarket = 'immediate' | '1_week' | '2_weeks' | '1_month' | 'flexible';
```

## Recommendation Process

### Step 1: Requirement Analysis
- Parse requirements from conversation, config, system prompt
- Validate against requirements schema
- Extract key constraints and priorities

### Step 2: Pattern Matching
- Analyze each pattern against requirements
- Weight patterns by requirement importance
- Calculate confidence scores

### Step 3: Recommendation Generation
- Identify best-fit pattern
- Provide tech stack recommendations
- Articulate trade-offs

### Step 4: Validation
- Ensure recommendation aligns with design principles
- Verify pattern can scale to projected size
- Check cost against budget constraints

## Usage Examples

### Example 1: Startup MVP
```
Requirements:
- Team: 2 frontend developers
- Timeline: 2 weeks to launch
- Budget: $0-500/month
- Complexity: Simple form + real-time dashboard
- Users: 100-1k initial

Recommendation: Lightweight SPA (Preact + Vite + Tailwind)
- Ultra-fast setup, minimal dependencies
- Bootstrap budget-friendly
- Sufficient for initial user base
```

### Example 2: Enterprise Application
```
Requirements:
- Team: 15 frontend developers
- Timeline: 12 weeks
- Budget: $5k+/month
- Complexity: Design system + 50+ pages
- Users: 10k+ concurrent

Recommendation: Component-Driven + Micro-Frontends
- Scalable for team size
- Strong type safety and reusability
- Independent team deployment
```

### Example 3: Content Platform
```
Requirements:
- Team: 3-5 developers
- Timeline: 4 weeks
- Budget: $500-1k/month
- Complexity: Content + search + comments
- Users: 100k+ monthly

Recommendation: Progressive Enhancement (Next.js)
- Excellent SEO and performance
- Content-first approach
- Server rendering for dynamic content
```

## Success Criteria

✅ Recommendations are adopted by development teams
✅ Recommended patterns remain effective through scale
✅ Technology choices support team growth
✅ Code maintains test coverage >80%
✅ Architecture enables fast iteration cycles

## Next Steps

1. Review current project requirements
2. Use the before_execution hook to generate recommendations
3. Validate recommendation against team capabilities
4. Begin implementation using generated guidance
5. Iterate based on real-world constraints

---

**Last Updated:** 2026-03-31
**Status:** Production Ready
**Maintenance:** Community-driven with enterprise support available
