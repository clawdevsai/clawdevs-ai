import { ArchitecturePattern } from "./architecture_matrix";
import { z } from "zod";

export interface Recommendation {
  patternId: string;
  patternName: string;
  framework: string;
  language: string;
  buildTool: string;
  styling: string;
  stateManagement: string;
  testing: string;
  reasoning: string;
  characteristics: Record<string, any>;
  costEstimate: Record<string, string>;
  tradeoffs: {
    advantages: string[];
    disadvantages: string[];
  };
  alternatives: string[];
  bestFor: string[];
  teamSize: string;
  scalableTo: string;
  confidence: number;
}

/**
 * Generate a recommendation from a selected pattern
 */
export function generateRecommendation(
  pattern: ArchitecturePattern,
  requirements: Record<string, any>,
  sources: string[]
): Recommendation {
  return {
    patternId: pattern.id,
    patternName: pattern.name,
    framework: pattern.framework,
    language: pattern.language,
    buildTool: pattern.buildTool,
    styling: pattern.styling,
    stateManagement: pattern.stateManagement,
    testing: pattern.testing,
    reasoning: pattern.reasoning,
    characteristics: pattern.characteristics,
    costEstimate: pattern.costEstimate,
    tradeoffs: pattern.tradeoffs,
    alternatives: pattern.alternatives,
    bestFor: pattern.bestFor,
    teamSize: pattern.teamSize,
    scalableTo: pattern.scalableTo,
    confidence: calculateConfidence(requirements, sources),
  };
}

/**
 * Format recommendation for human readability
 */
export function formatRecommendation(rec: Recommendation): string {
  const lines = [
    `## Recommended Frontend Architecture: ${rec.patternName}`,
    ``,
    `**Confidence Level:** ${rec.confidence}%`,
    `**Pattern ID:** ${rec.patternId}`,
    ``,
    `### Technology Stack`,
    `- **Framework:** ${rec.framework}`,
    `- **Language:** ${rec.language}`,
    `- **Build Tool:** ${rec.buildTool}`,
    `- **Styling:** ${rec.styling}`,
    `- **State Management:** ${rec.stateManagement}`,
    `- **Testing:** ${rec.testing}`,
    ``,
    `### Rationale`,
    `${rec.reasoning}`,
    ``,
    `### Why This Pattern Works for Your Project`,
    `Best suited for: ${rec.bestFor.join(", ")}`,
    `Team size: ${rec.teamSize}`,
    `Scalable to: ${rec.scalableTo}`,
    ``,
    `### Characteristics`,
    ...Object.entries(rec.characteristics).map(([key, value]) => `- **${formatKey(key)}:** ${value}`),
    ``,
    `### Cost Estimate`,
    ...Object.entries(rec.costEstimate).map(([key, value]) => `- **${formatKey(key)}:** ${value}`),
    ``,
    `### Trade-offs`,
    `**Advantages:**`,
    ...rec.tradeoffs.advantages.map((a) => `- ✅ ${a}`),
    ``,
    `**Disadvantages:**`,
    ...rec.tradeoffs.disadvantages.map((d) => `- ❌ ${d}`),
    ``,
    `### Alternative Approaches`,
    ...rec.alternatives.slice(0, 2).map((alt) => `- ${alt}`),
    ``,
  ];

  return lines.join("\n");
}

function formatKey(key: string): string {
  return key
    .replace(/_/g, " ")
    .replace(/([A-Z])/g, " $1")
    .trim()
    .split(" ")
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

/**
 * Calculate confidence based on requirement source quality
 */
function calculateConfidence(requirements: Record<string, any>, sources: string[]): number {
  let baseConfidence = 70; // Default 70%

  // Increase confidence if multiple sources
  if (sources.length > 1) {
    baseConfidence += 10;
  }

  // Increase confidence if detailed requirements
  const detailedFields = Object.values(requirements).filter((v) => v !== undefined && v !== null).length;
  if (detailedFields >= 4) {
    baseConfidence += 10;
  }

  return Math.min(baseConfidence, 95); // Cap at 95%
}

/**
 * Get all available patterns
 */
export function getAllPatterns(): string[] {
  return [
    "component_driven",
    "progressive_enhancement",
    "micro_frontend",
    "lightweight_spa",
    "headless_cms",
    "fullstack_monolith",
  ];
}

/**
 * Get pattern by ID
 */
export function getPatternByName(name: string): string | undefined {
  const mapping: Record<string, string> = {
    "Component-Driven Architecture": "component_driven",
    "Progressive Enhancement": "progressive_enhancement",
    "Micro-Frontend Architecture": "micro_frontend",
    "Lightweight SPA": "lightweight_spa",
    "Headless CMS": "headless_cms",
    "Full-Stack Monolith": "fullstack_monolith",
  };
  return mapping[name];
}

/**
 * Compare patterns
 */
export function comparePatterns(pattern1: Recommendation, pattern2: Recommendation): Record<string, any> {
  return {
    framework: {
      pattern1: pattern1.framework,
      pattern2: pattern2.framework,
    },
    language: {
      pattern1: pattern1.language,
      pattern2: pattern2.language,
    },
    buildTool: {
      pattern1: pattern1.buildTool,
      pattern2: pattern2.buildTool,
    },
    styleSystem: {
      pattern1: pattern1.styling,
      pattern2: pattern2.styling,
    },
    teamSize: {
      pattern1: pattern1.teamSize,
      pattern2: pattern2.teamSize,
    },
    costEstimate: {
      pattern1: pattern1.costEstimate.infrastructure,
      pattern2: pattern2.costEstimate.infrastructure,
    },
    developmentTime: {
      pattern1: pattern1.costEstimate.development,
      pattern2: pattern2.costEstimate.development,
    },
  };
}
