import { findMatchingPattern, getPatternById } from "../decisions/patterns";
import { generateRecommendation, formatRecommendation } from "../decisions/recommendations";
import { parseRequirements } from "../utils/requirement-parser";
import { Logger } from "../utils/logger";
import { requirementsSchema } from "../schemas/requirements";

const logger = new Logger("memory_curator:before_execution");

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

export async function beforeExecutionHook(
  input: BeforeExecutionInput
): Promise<BeforeExecutionOutput> {
  const startTime = Date.now();
  logger.info("Analysis started", {
    hasConversation: !!input.conversation,
    hasConfig: !!input.projectConfig,
    hasSystemPrompt: !!input.systemPrompt,
  });

  try {
    const requirements = parseRequirements({
      conversation: input.conversation,
      projectConfig: input.projectConfig,
      systemPrompt: input.systemPrompt,
    });

    const validatedRequirements = requirementsSchema.parse(requirements.parsed);
    logger.info("Requirements validated", { validatedRequirements });

    const { pattern, score, alternatives } = findMatchingPattern({});

    logger.info("Pattern matched", {
      pattern: pattern.id,
      confidence: score,
    });

    const recommendation = generateRecommendation(pattern, validatedRequirements, requirements.sources);
    const formattedRecommendation = formatRecommendation(recommendation);

    const executionTime = Date.now() - startTime;
    logger.info("Analysis completed", { executionTime });

    return {
      success: true,
      recommendation: {
        patternId: pattern.id,
        patternName: pattern.name,
        confidence: score,
        reasoning: pattern.reasoning,
        characteristics: pattern.characteristics,
        costEstimate: pattern.costEstimate,
        tradeoffs: pattern.tradeoffs,
        alternatives: alternatives.map((alt) => ({
          patternId: alt.pattern.id,
          patternName: alt.pattern.name,
          confidence: alt.score,
        })),
        nextSteps: recommendation.nextSteps,
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
    logger.error("Analysis failed", {
      error: error instanceof Error ? error.message : String(error),
      executionTime,
    });

    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error",
      executionTime,
    };
  }
}

export default beforeExecutionHook;
