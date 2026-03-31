/**
 * Pattern definitions for agent_reviver
 */

export interface Pattern {
  id: string;
  name: string;
  description: string;
  language: string;
  maturity: "experimental" | "beta" | "production";
  reasoning: string;
  characteristics: Record<string, any>;
  tradeoffs: {
    advantages: string[];
    disadvantages: string[];
  };
  costEstimate: Record<string, string>;
}

export const patterns: Record<string, Pattern> = {
  primary_pattern: {
    id: "primary_pattern",
    name: "Primary Pattern",
    description: "Recommended pattern for standard requirements",
    language: "typescript",
    maturity: "production",
    reasoning: "Balanced approach across all dimensions",
    characteristics: {
      scalability: "high",
      maintainability: "high",
      complexity: "moderate",
    },
    tradeoffs: {
      advantages: ["Scalable", "Maintainable", "Well-documented"],
      disadvantages: ["Higher initial setup", "Learning curve"],
    },
    costEstimate: {
      infrastructure: "$1k-5k/month",
      development: "2-4 weeks",
    },
  },
  alternative_pattern: {
    id: "alternative_pattern",
    name: "Alternative Pattern",
    description: "Alternative approach for specific constraints",
    language: "typescript",
    maturity: "production",
    reasoning: "Optimized for different trade-offs",
    characteristics: {
      scalability: "moderate",
      maintainability: "moderate",
      complexity: "low",
    },
    tradeoffs: {
      advantages: ["Simpler", "Faster setup", "Lower cost"],
      disadvantages: ["Limited scalability", "Less flexible"],
    },
    costEstimate: {
      infrastructure: "$100-1k/month",
      development: "1-2 weeks",
    },
  },
};

export function scorePattern(pattern: Pattern, requirements: Record<string, number>): number {
  let score = 50;
  // Score calculation logic
  return Math.min(100, Math.max(0, score));
}

export function findMatchingPattern(requirements: Record<string, number>) {
  const allPatterns = Object.values(patterns);
  const scored = allPatterns.map((pattern) => ({
    pattern,
    score: scorePattern(pattern, requirements),
  }));

  scored.sort((a, b) => b.score - a.score);

  return {
    pattern: scored[0].pattern,
    score: scored[0].score,
    alternatives: scored.slice(1, 3),
  };
}

export function getPatternById(id: string): Pattern | undefined {
  return patterns[id];
}

export function getAllPatterns(): Pattern[] {
  return Object.values(patterns);
}

export function comparePatterns(id1: string, id2: string): { winner: string; reasoning: string } {
  const p1 = patterns[id1];
  const p2 = patterns[id2];

  if (!p1 || !p2) {
    return { winner: "none", reasoning: "Pattern not found" };
  }

  return {
    winner: p1.id,
    reasoning: "Primary pattern is recommended",
  };
}
