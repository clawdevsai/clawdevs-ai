import { findMatchingPattern, getPatternById } from "../decisions/architecture_matrix";
import { generateRecommendation, formatRecommendation } from "../decisions/recommendations";
import { parseRequirements } from "../utils/requirement-parser";
import { Logger } from "../utils/logger";
import { requirementsSchema } from "../schemas/requirements";
import { z } from "zod";

const logger = new Logger("dev_frontend:before_execution");

/**
 * Hook interface for before_execution
 */
export interface BeforeExecutionInput {
  conversation?: string;
  projectConfig?: Record<string, any>;
  systemPrompt?: string;
  userContext?: Record<string, any>;
}

export interface BeforeExecutionOutput {
  success: boolean;
  recommendation?: {
    patternId: string;
    patternName: string;
    confidence: number;
    reasoning: string;
    techStack: {
      framework: string;
      language: string;
      buildTool: string;
      styling: string;
      stateManagement: string;
      testing: string;
    };
    characteristics: Record<string, any>;
    costEstimate: Record<string, string>;
    tradeoffs: {
      advantages: string[];
      disadvantages: string[];
    };
    alternatives: Array<{
      patternId: string;
      patternName: string;
      confidence: number;
    }>;
    nextSteps: string[];
  };
  analysis?: {
    detectedRequirements: Record<string, any>;
    requirementSources: string[];
    confidence: number;
    warnings: string[];
  };
  error?: string;
  executionTime?: number;
}

/**
 * Main before_execution hook for frontend implementation
 *
 * Analyzes project requirements from multiple sources (conversation, config, system prompt)
 * and recommends the optimal frontend architecture pattern with complete tech stack guidance.
 */
export async function beforeExecutionHook(
  input: BeforeExecutionInput
): Promise<BeforeExecutionOutput> {
  const startTime = Date.now();
  logger.info("Frontend architecture analysis started", {
    hasCon versation: !!input.conversation,
    hasConfig: !!input.projectConfig,
    hasSystemPrompt: !!input.systemPrompt,
  });

  try {
    // Step 1: Parse requirements from all sources with cascade fallback
    logger.debug("Parsing requirements from multiple sources");
    const requirements = parseRequirements({
      conversation: input.conversation,
      projectConfig: input.projectConfig,
      systemPrompt: input.systemPrompt,
      domain: "frontend",
    });

    // Validate requirements against schema
    const validatedRequirements = requirementsSchema.parse(requirements.parsed);
    logger.info("Requirements validated successfully", { validatedRequirements });

    // Step 2: Find matching pattern
    logger.debug("Matching requirements to architecture patterns");
    const { pattern, score, alternatives } = findMatchingPattern({
      volume: requirements.parsed.volume ? mapVolumeToScore(requirements.parsed.volume) : undefined,
      latency: requirements.parsed.latency ? mapLatencyToScore(requirements.parsed.latency) : undefined,
      costSensitivity: requirements.parsed.costSensitivity
        ? mapCostToScore(requirements.parsed.costSensitivity)
        : undefined,
      reliability: requirements.parsed.reliability
        ? mapReliabilityToScore(requirements.parsed.reliability)
        : undefined,
      uiComplexity: requirements.parsed.uiComplexity
        ? mapUIComplexityToScore(requirements.parsed.uiComplexity)
        : undefined,
      timeToMarket: requirements.parsed.timeToMarket
        ? mapTimeToMarketToScore(requirements.parsed.timeToMarket)
        : undefined,
    });

    logger.info("Pattern matching completed", {
      selectedPattern: pattern.id,
      confidence: score,
      alternatives: alternatives.map((a) => ({ pattern: a.pattern.id, score: a.score })),
    });

    // Step 3: Generate recommendation
    logger.debug("Generating detailed recommendation");
    const recommendation = generateRecommendation(pattern, validatedRequirements, requirements.sources);

    // Step 4: Format output
    const formattedRecommendation = formatRecommendation(recommendation);

    const nextSteps = [
      `1. Review the ${pattern.name} pattern recommendation`,
      `2. Validate team has required expertise (${pattern.language}, ${pattern.framework})`,
      `3. Review cost estimate: ${pattern.costEstimate.infrastructure}`,
      `4. Timeline estimate: ${pattern.costEstimate.development}`,
      `5. Set up development environment with ${pattern.buildTool}`,
      `6. Initialize test infrastructure (${pattern.testing})`,
      `7. Begin component development with design system approach`,
      `8. Implement CI/CD pipeline for automated testing`,
    ];

    const executionTime = Date.now() - startTime;
    logger.info("Frontend architecture analysis completed successfully", {
      executionTime,
      pattern: pattern.id,
      confidence: score,
    });

    return {
      success: true,
      recommendation: {
        patternId: pattern.id,
        patternName: pattern.name,
        confidence: score,
        reasoning: pattern.reasoning,
        techStack: {
          framework: pattern.framework,
          language: pattern.language,
          buildTool: pattern.buildTool,
          styling: pattern.styling,
          stateManagement: pattern.stateManagement,
          testing: pattern.testing,
        },
        characteristics: pattern.characteristics,
        costEstimate: pattern.costEstimate,
        tradeoffs: pattern.tradeoffs,
        alternatives: alternatives.map((alt) => ({
          patternId: alt.pattern.id,
          patternName: alt.pattern.name,
          confidence: alt.score,
        })),
        nextSteps,
      },
      analysis: {
        detectedRequirements: validatedRequirements,
        requirementSources: requirements.sources,
        confidence: score,
        warnings: [],
      },
      executionTime,
    };
  } catch (error) {
    const executionTime = Date.now() - startTime;
    logger.error("Frontend architecture analysis failed", {
      error: error instanceof Error ? error.message : String(error),
      executionTime,
    });

    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error during analysis",
      executionTime,
    };
  }
}

// Helper functions to map requirement values to scores

function mapVolumeToScore(volume: string): number {
  const mapping: Record<string, number> = {
    small: 20,
    medium: 50,
    large: 80,
    xlarge: 100,
  };
  return mapping[volume] || 50;
}

function mapLatencyToScore(latency: string): number {
  const mapping: Record<string, number> = {
    realtime: 100,
    sub_100ms: 90,
    sub_500ms: 70,
    sub_2s: 40,
    flexible: 10,
  };
  return mapping[latency] || 50;
}

function mapCostToScore(costSensitivity: string): number {
  const mapping: Record<string, number> = {
    critical: 100,
    high: 80,
    moderate: 50,
    low: 20,
    irrelevant: 10,
  };
  return mapping[costSensitivity] || 50;
}

function mapReliabilityToScore(reliability: string): number {
  const mapping: Record<string, number> = {
    mission_critical: 100,
    high: 75,
    moderate: 50,
    low: 25,
  };
  return mapping[reliability] || 50;
}

function mapUIComplexityToScore(uiComplexity: string): number {
  const mapping: Record<string, number> = {
    highly_complex: 100,
    complex: 80,
    moderate: 50,
    simple: 20,
  };
  return mapping[uiComplexity] || 50;
}

function mapTimeToMarketToScore(timeToMarket: string): number {
  const mapping: Record<string, number> = {
    immediate: 100,
    one_week: 90,
    two_weeks: 80,
    one_month: 50,
    flexible: 10,
  };
  return mapping[timeToMarket] || 50;
}

export default beforeExecutionHook;
