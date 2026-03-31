import { Requirements } from "../schemas/requirements";
import { Logger } from "./logger";

const logger = new Logger("requirement-parser");

/**
 * Parse requirements from multiple sources with cascade fallback
 */
export function parseRequirements(input: {
  conversation?: string;
  projectConfig?: Record<string, any>;
  systemPrompt?: string;
  domain?: string;
}): {
  parsed: Requirements;
  sources: string[];
  confidence: number;
} {
  const requirements: Requirements = {};
  const sources: string[] = [];

  // Priority: conversation > projectConfig > systemPrompt
  if (input.conversation) {
    const conversationReqs = parseConversation(input.conversation);
    Object.assign(requirements, conversationReqs);
    sources.push("conversation");
    logger.debug("Parsed requirements from conversation", { conversationReqs });
  }

  if (input.projectConfig) {
    const configReqs = parseProjectConfig(input.projectConfig);
    // Only add if not already set from conversation
    Object.entries(configReqs).forEach(([key, value]) => {
      if (!(key in requirements) && value !== undefined) {
        (requirements as any)[key] = value;
      }
    });
    sources.push("projectConfig");
    logger.debug("Parsed requirements from projectConfig", { configReqs });
  }

  if (input.systemPrompt) {
    const systemReqs = parseSystemPrompt(input.systemPrompt);
    // Only add if not already set
    Object.entries(systemReqs).forEach(([key, value]) => {
      if (!(key in requirements) && value !== undefined) {
        (requirements as any)[key] = value;
      }
    });
    sources.push("systemPrompt");
    logger.debug("Parsed requirements from systemPrompt", { systemReqs });
  }

  const confidence = calculateConfidence(requirements, sources);
  logger.info("Requirements parsing completed", { sources, confidence });

  return { parsed: requirements, sources, confidence };
}

/**
 * Parse requirements from conversation text
 */
function parseConversation(text: string): Requirements {
  const requirements: Requirements = {};

  // Volume detection
  if (text.match(/\b(small|tiny|simple|just a)/i)) {
    requirements.volume = "small";
  } else if (text.match(/\b(medium|moderate|mid-size|mid)\b/i)) {
    requirements.volume = "medium";
  } else if (text.match(/\b(large|big|substantial|significant)\b/i)) {
    requirements.volume = "large";
  } else if (text.match(/\b(huge|massive|enterprise|global|world|scale)\b/i)) {
    requirements.volume = "xlarge";
  }

  // Latency detection
  if (text.match(/\b(realtime|real-time|instant|immediate)\b/i)) {
    requirements.latency = "realtime";
  } else if (text.match(/\b(fast|quick|under 100|<100ms|sub-100)\b/i)) {
    requirements.latency = "sub_100ms";
  } else if (text.match(/\b(responsive|under 500|<500ms|sub-500)\b/i)) {
    requirements.latency = "sub_500ms";
  } else if (text.match(/\b(2 seconds?|2s|2000ms)\b/i)) {
    requirements.latency = "sub_2s";
  } else if (text.match(/\b(performance|speed|slow|latency)\b/i)) {
    requirements.latency = "flexible";
  }

  // Cost sensitivity detection
  if (text.match(/\b(bootstrap|startup|budget|cheap|free|no budget|minimal cost)\b/i)) {
    requirements.costSensitivity = "critical";
  } else if (text.match(/\b(cost-conscious|cost-aware|budget-friendly|limited budget)\b/i)) {
    requirements.costSensitivity = "high";
  } else if (text.match(/\b(reasonable|moderate|balanced cost)\b/i)) {
    requirements.costSensitivity = "moderate";
  } else if (text.match(/\b(generous|unlimited|no limit|as needed)\b/i)) {
    requirements.costSensitivity = "irrelevant";
  }

  // Reliability detection
  if (text.match(/\b(99\.99%|mission.critical|critical|financial|banking|healthcare)\b/i)) {
    requirements.reliability = "mission_critical";
  } else if (text.match(/\b(high.*reliability|very reliable|99\.9%|production)\b/i)) {
    requirements.reliability = "high";
  } else if (text.match(/\b(reliable|stable|good uptime)\b/i)) {
    requirements.reliability = "moderate";
  }

  // UI Complexity detection
  if (text.match(/\b(simple|form|basic|straightforward)\b/i)) {
    requirements.uiComplexity = "simple";
  } else if (text.match(/\b(moderate|medium|standard|typical)\b/i)) {
    requirements.uiComplexity = "moderate";
  } else if (text.match(/\b(complex|interactive|sophisticated|advanced)\b/i)) {
    requirements.uiComplexity = "complex";
  } else if (text.match(/\b(highly complex|rich|immersive|dashboards|design system)\b/i)) {
    requirements.uiComplexity = "highly_complex";
  }

  // Time to market detection
  if (text.match(/\b(now|asap|today|this week|immediate|launch today)\b/i)) {
    requirements.timeToMarket = "immediate";
  } else if (text.match(/\b(week|7 days?)\b/i)) {
    requirements.timeToMarket = "one_week";
  } else if (text.match(/\b(2 weeks?|14 days?|two weeks)\b/i)) {
    requirements.timeToMarket = "two_weeks";
  } else if (text.match(/\b(month|4 weeks?|30 days?)\b/i)) {
    requirements.timeToMarket = "one_month";
  } else if (text.match(/\b(flexible|whenever|no deadline)\b/i)) {
    requirements.timeToMarket = "flexible";
  }

  return requirements;
}

/**
 * Parse requirements from project configuration
 */
function parseProjectConfig(config: Record<string, any>): Requirements {
  const requirements: Requirements = {};

  // Try to extract from nested config
  const frontend = config.frontend || config.ui || {};
  const project = config.project || {};

  if (frontend.volume || project.volume) {
    requirements.volume = frontend.volume || project.volume;
  }

  if (frontend.latency || project.latency) {
    requirements.latency = frontend.latency || project.latency;
  }

  if (frontend.costSensitivity || project.costSensitivity) {
    requirements.costSensitivity = frontend.costSensitivity || project.costSensitivity;
  }

  if (frontend.reliability || project.reliability) {
    requirements.reliability = frontend.reliability || project.reliability;
  }

  if (frontend.uiComplexity || project.uiComplexity) {
    requirements.uiComplexity = frontend.uiComplexity || project.uiComplexity;
  }

  if (frontend.timeToMarket || project.timeToMarket) {
    requirements.timeToMarket = frontend.timeToMarket || project.timeToMarket;
  }

  return requirements;
}

/**
 * Parse requirements from system prompt
 */
function parseSystemPrompt(prompt: string): Requirements {
  // Use same parsing as conversation
  return parseConversation(prompt);
}

/**
 * Calculate confidence score based on source quality
 */
function calculateConfidence(requirements: Requirements, sources: string[]): number {
  let confidence = 50; // Base confidence

  // Increase for multiple sources
  if (sources.length > 1) confidence += 15;
  if (sources.length > 2) confidence += 10;

  // Increase based on number of requirements specified
  const specifiedCount = Object.values(requirements).filter((v) => v !== undefined).length;
  if (specifiedCount >= 3) confidence += 15;
  if (specifiedCount >= 5) confidence += 10;

  // Explicit config source is most reliable
  if (sources.includes("projectConfig")) confidence += 10;

  return Math.min(confidence, 95);
}
