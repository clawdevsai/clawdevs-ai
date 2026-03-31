export { beforeExecutionHook } from "./hooks/before_execution";
export type { BeforeExecutionInput, BeforeExecutionOutput } from "./hooks/before_execution";

export {
  architecturePatterns,
  scorePattern,
  findMatchingPattern,
  getPatternById,
  getAllPatterns,
  comparePatterns,
} from "./decisions/architecture_matrix";
export type { ArchitecturePattern } from "./decisions/architecture_matrix";

export { generateRecommendation, formatRecommendation } from "./decisions/recommendations";
export type { Recommendation } from "./decisions/recommendations";

export { parseRequirements } from "./utils/requirement-parser";
export { Logger } from "./utils/logger";
export type { LogEntry } from "./utils/logger";

export { requirementsSchema, VolumeEnum, LatencyEnum, CostSensitivityEnum, ReliabilityEnum, UIComplexityEnum, TimeToMarketEnum } from "./schemas/requirements";
export type { Requirements } from "./schemas/requirements";
