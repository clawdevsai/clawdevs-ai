export { beforeExecutionHook } from "./hooks/before_execution";
export type { BeforeExecutionInput, BeforeExecutionOutput } from "./hooks/before_execution";

export {
  patterns,
  scorePattern,
  findMatchingPattern,
  getPatternById,
  getAllPatterns,
  comparePatterns,
} from "./decisions/patterns";
export type { Pattern } from "./decisions/patterns";

export { generateRecommendation, formatRecommendation } from "./decisions/recommendations";
export type { Recommendation } from "./decisions/recommendations";

export { parseRequirements } from "./utils/requirement-parser";
export { Logger } from "./utils/logger";
export type { LogEntry } from "./utils/logger";

export { requirementsSchema } from "./schemas/requirements";
export type { Requirements } from "./schemas/requirements";
