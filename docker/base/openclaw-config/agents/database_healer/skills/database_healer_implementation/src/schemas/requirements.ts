import { z } from "zod";

/**
 * Requirements schema for database_healer analysis
 */

export const ScaleEnum = z.enum(["small", "medium", "large", "xlarge"]);
export const PriorityEnum = z.enum(["critical", "high", "medium", "low"]);
export const ConstraintEnum = z.enum(["time", "budget", "resources", "technical", "none"]);
export const RiskEnum = z.enum(["low", "moderate", "high", "critical"]);

export const requirementsSchema = z.object({
  scale: ScaleEnum.optional(),
  priority: PriorityEnum.optional(),
  constraint: ConstraintEnum.optional(),
  risk: RiskEnum.optional(),
  description: z.string().optional(),
  context: z.record(z.any()).optional(),
});

export type Requirements = z.infer<typeof requirementsSchema>;
