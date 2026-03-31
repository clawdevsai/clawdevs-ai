import { z } from "zod";

/**
 * Requirements schema for frontend architecture analysis
 */

export const VolumeEnum = z.enum(["small", "medium", "large", "xlarge"]);
export const LatencyEnum = z.enum(["realtime", "sub_100ms", "sub_500ms", "sub_2s", "flexible"]);
export const CostSensitivityEnum = z.enum(["critical", "high", "moderate", "low", "irrelevant"]);
export const ReliabilityEnum = z.enum(["low", "moderate", "high", "mission_critical"]);
export const UIComplexityEnum = z.enum(["simple", "moderate", "complex", "highly_complex"]);
export const TimeToMarketEnum = z.enum(["immediate", "one_week", "two_weeks", "one_month", "flexible"]);

export const requirementsSchema = z.object({
  volume: VolumeEnum.optional(),
  latency: LatencyEnum.optional(),
  costSensitivity: CostSensitivityEnum.optional(),
  reliability: ReliabilityEnum.optional(),
  uiComplexity: UIComplexityEnum.optional(),
  timeToMarket: TimeToMarketEnum.optional(),
});

export type Requirements = z.infer<typeof requirementsSchema>;
