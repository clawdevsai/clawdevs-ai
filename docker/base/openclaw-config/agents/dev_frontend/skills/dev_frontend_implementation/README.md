# dev_frontend Implementation

Frontend architecture analysis, technology selection, and scalable UI patterns for modern web applications.

**Version:** 2.0.0
**Status:** Production Ready

## Quick Start

This skill provides intelligent frontend architecture recommendations based on your project requirements.

### 1. Basic Usage

```typescript
import { beforeExecutionHook } from "./src/hooks/before_execution";

const result = await beforeExecutionHook({
  conversation: "We need a fast-loading e-commerce site that can handle 100k users",
  projectConfig: {
    frontend: {
      volume: "xlarge",
      latency: "sub_500ms",
      costSensitivity: "moderate",
    },
  },
});

if (result.success && result.recommendation) {
  console.log(`Recommended: ${result.recommendation.patternName}`);
  console.log(`Tech Stack: ${result.recommendation.techStack.framework}`);
  console.log(`Confidence: ${result.recommendation.confidence}%`);
}
```

### 2. Architecture Patterns

#### Component-Driven (React/Vue/Angular)
Best for: Complex UIs, Design Systems, Large Teams
- Complexity: 50k-500k+ LOC
- Team: 10-50 developers
- Cost: $2k-5k/month

#### Progressive Enhancement (Next.js/Nuxt)
Best for: E-commerce, Content Platforms
- Complexity: ~200k LOC
- Team: 5-20 developers
- Cost: $500-2k/month

#### Micro-Frontend Architecture
Best for: Large Organizations, Independent Teams
- Complexity: 1M+ LOC
- Team: 20-100 developers
- Cost: $5k-10k/month

#### Lightweight SPA (Vanilla/Preact)
Best for: MVPs, Performance-Critical
- Complexity: 5k-20k LOC
- Team: 1-5 developers
- Cost: $0-500/month

#### Headless CMS + Static
Best for: Content Sites, Marketing
- Complexity: 100k+ pages
- Team: 2-10 developers
- Cost: $100-1k/month

#### Full-Stack Monolith
Best for: Legacy Systems, Gradual Migration
- Complexity: ~50k LOC
- Team: 3-10 developers
- Cost: $1k-3k/month

## Real-World Examples

### Example 1: Startup MVP (2-week Launch)
```javascript
// Requirements: Quick launch, minimal budget
const result = await beforeExecutionHook({
  conversation: "We have 2 weeks and $500/month budget"
});

// Result: Lightweight SPA (Preact + Tailwind + Vite)
// - Deploy in 1 week
// - $0-500/month
// - Perfect for initial users
```

### Example 2: E-Commerce Platform (Scaling)
```javascript
// Requirements: Fast performance, SEO important, growth mindset
const result = await beforeExecutionHook({
  conversation: "E-commerce site, 100k monthly users, need SEO"
});

// Result: Progressive Enhancement (Next.js)
// - Excellent SEO performance
// - Fast FCP/LCP metrics
// - Server-side rendering
// - $500-2k/month
```

### Example 3: Enterprise Application
```javascript
// Requirements: Large team, complex UI, long-term
const result = await beforeExecutionHook({
  projectConfig: {
    frontend: {
      volume: "xlarge",
      uiComplexity: "highly_complex",
      timeToMarket: "one_month"
    }
  }
});

// Result: Component-Driven Architecture
// - React + TypeScript + Design System
// - Component library with Storybook
// - Design tokens for consistency
// - $2k-5k/month
```

## Architecture Comparison

| Pattern | Framework | Bundle | SEO | Interactive | Scalability | Cost |
|---------|-----------|--------|-----|-------------|-------------|------|
| Component-Driven | React/Vue | Medium | Fair | Excellent | Excellent | High |
| Progressive | Next.js | Small | Excellent | Good | Excellent | Medium |
| Micro-Frontend | React+Fed | Large | Fair | Excellent | Unlimited | High |
| Lightweight | Preact | Tiny | Fair | Fair | Limited | Low |
| Static | 11ty | Tiny | Excellent | Limited | Excellent | Low |
| Monolith | Express | Large | Excellent | Fair | Limited | Medium |

## Design Principles

All recommendations follow:
- **SOLID** - Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **KISS** - Keep It Simple, Stupid
- **YAGNI** - You Aren't Gonna Need It
- **DRY** - Don't Repeat Yourself
- **DDD** - Domain-Driven Design
- **TDD** - Test-Driven Development

## Testing

Run the comprehensive test suite:

```bash
npm test                    # Run all tests
npm run test:watch         # Watch mode
npm run test:coverage      # Coverage report
```

**Coverage Target:** >80%
- Decisions & Patterns: 95%+ coverage
- Recommendations: 90%+ coverage
- Integration: 85%+ coverage

## Documentation

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) - System design and architecture
- [`docs/PRINCIPLES.md`](docs/PRINCIPLES.md) - Design principles applied
- [`docs/TESTING.md`](docs/TESTING.md) - Test strategy and coverage
- [`docs/GETTING_STARTED.md`](docs/GETTING_STARTED.md) - Detailed getting started guide

## Next Steps

1. Review your project requirements
2. Use the `beforeExecutionHook` to get recommendations
3. Validate recommendation with your team
4. Follow the technology stack guidance
5. Use the Next Steps provided in the recommendation

---

**Maintained by:** clawdevs-ai
**License:** MIT
**Last Updated:** 2026-03-31
