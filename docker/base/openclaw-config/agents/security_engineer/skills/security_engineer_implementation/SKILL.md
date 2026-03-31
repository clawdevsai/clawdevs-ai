# security_engineer Implementation Skill

**Version:** 2.0.0
**Maturity:** Production
**Scope:** Security patterns and vulnerability analysis

## Overview

This skill analyzes security requirements and recommends comprehensive security patterns and controls. It evaluates threat models, implements defense-in-depth strategies, and recommends security best practices for authentication, authorization, encryption, and vulnerability management. The system provides production-grade security architecture guidance grounded in OWASP, CWE, and industry standards.

The intelligent `before_execution` hook analyzes requirements from multiple sources (conversation, project config, system prompts) and recommends optimal patterns and best practices. The system uses a production-grade pattern matching algorithm with weighted scoring to ensure decisions align with industry standards and proven practices.

## Core Values

1. **Flow** - Uninterrupted development velocity, clear decision-making
2. **Quality Gates** - Enforced standards at every stage
3. **Guardrails** - Prevent anti-patterns and technical debt

## Key Responsibilities

- **Intelligent Analysis**: Parse requirements from multiple sources with cascade fallback
- **Pattern Matching**: Match requirements to optimal patterns
- **Recommendation Generation**: Provide actionable recommendations
- **Trade-off Analysis**: Articulate pros/cons for recommended approaches
- **Pattern Validation**: Ensure recommendations follow best practices

## Design Principles

All recommendations are grounded in industry best practices:

- **SOLID Principles**: Clean, maintainable architecture
- **KISS** (Keep It Simple, Stupid): Prefer straightforward solutions
- **YAGNI** (You Aren't Gonna Need It): Avoid speculative features
- **DRY** (Don't Repeat Yourself): Reusable components and utilities
- **Domain-Driven Design**: Business logic expressed in domain language
- **Test-Driven Development**: Tests drive architecture and design
- **Clean Code**: Clear naming, small functions, focused responsibilities

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
- Provide actionable recommendations
- Articulate trade-offs

### Step 4: Validation
- Ensure recommendation aligns with best practices
- Verify pattern can scale to projected requirements
- Check constraints are met

## Success Criteria

✅ Recommendations are adopted by development teams
✅ Recommended patterns remain effective through scale
✅ Decisions support team growth and capability expansion
✅ Code maintains high quality standards
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
