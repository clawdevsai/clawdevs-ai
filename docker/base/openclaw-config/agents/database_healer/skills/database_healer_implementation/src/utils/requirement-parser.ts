import { Requirements } from "../schemas/requirements";

export interface ParserInput {
  conversation?: string;
  projectConfig?: Record<string, any>;
  systemPrompt?: string;
  domain?: string;
}

export interface ParsedRequirements {
  parsed: Requirements;
  sources: string[];
  confidence: number;
}

/**
 * Parse requirements from multiple sources with cascade fallback
 */
export function parseRequirements(input: ParserInput): ParsedRequirements {
  const sources: string[] = [];
  const requirements: Partial<Requirements> = {};
  let confidence = 0;

  // Cascade fallback: conversation > projectConfig > systemPrompt
  if (input.conversation) {
    sources.push("conversation");
    confidence = Math.max(confidence, 0.8);
  }

  if (input.projectConfig) {
    sources.push("projectConfig");
    confidence = Math.max(confidence, 0.7);
  }

  if (input.systemPrompt) {
    sources.push("systemPrompt");
    confidence = Math.max(confidence, 0.6);
  }

  return {
    parsed: requirements as Requirements,
    sources,
    confidence: Math.min(confidence, 1.0),
  };
}
