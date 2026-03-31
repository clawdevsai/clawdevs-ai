import { z } from 'zod';

/**
 * Volume enum - Defines the scale of requests the system must handle
 * - low: Less than 1,000 requests/second
 * - medium: 1,000 to 100,000 requests/second
 * - high: 100,000 to 1,000,000 requests/second
 * - extreme: More than 1,000,000 requests/second
 */
export const VolumeRequirement = z.enum(['low', 'medium', 'high', 'extreme']);
export type VolumeRequirement = z.infer<typeof VolumeRequirement>;

/**
 * Latency enum - Defines the acceptable response time for operations
 * - relaxed: Less than 5 seconds (batch/background jobs)
 * - normal: Less than 1 second (regular operations)
 * - responsive: Less than 500ms (user-facing operations)
 * - realtime: Less than 100ms (interactive operations)
 * - ultra: Less than 10ms (ultra-low latency, real-time streaming)
 */
export const LatencyRequirement = z.enum(['relaxed', 'normal', 'responsive', 'realtime', 'ultra']);
export type LatencyRequirement = z.infer<typeof LatencyRequirement>;

/**
 * CostSensitivity enum - Defines budget constraints and operational costs
 * - unlimited: No budget constraints
 * - low: Minimize costs at the expense of other factors
 * - medium: Balanced cost and performance
 * - high: Cost is a critical constraint, prefer cheaper solutions
 */
export const CostSensitivity = z.enum(['unlimited', 'low', 'medium', 'high']);
export type CostSensitivity = z.infer<typeof CostSensitivity>;

/**
 * Reliability enum - Defines the required system uptime and SLA
 * - best_effort: 95%+ uptime (typical web services)
 * - acceptable: 99%+ uptime (standard SLA)
 * - critical: 99.9%+ uptime (mission-critical systems)
 * - highly_critical: 99.99%+ uptime (financial, healthcare systems)
 */
export const Reliability = z.enum(['best_effort', 'acceptable', 'critical', 'highly_critical']);
export type Reliability = z.infer<typeof Reliability>;

/**
 * DataComplexity enum - Defines the complexity of data structures and relationships
 * - simple: CRUD operations on flat structures
 * - moderate: Relationships between entities, basic joins
 * - complex: Graph-like structures, complex relationships
 * - extreme: Machine learning pipelines, real-time analytics, streaming data
 */
export const DataComplexity = z.enum(['simple', 'moderate', 'complex', 'extreme']);
export type DataComplexity = z.infer<typeof DataComplexity>;

/**
 * TimeToMarket enum - Defines the urgency of deployment
 * - asap: Days to weeks
 * - normal: Weeks to months
 * - flexible: Months or longer, allowing for optimization
 */
export const TimeToMarket = z.enum(['asap', 'normal', 'flexible']);
export type TimeToMarket = z.infer<typeof TimeToMarket>;

/**
 * RequirementsSchema - Defines all non-functional requirements for a system
 */
export const RequirementsSchema = z.object({
  volume: VolumeRequirement,
  latency: LatencyRequirement,
  costSensitivity: CostSensitivity,
  reliability: Reliability,
  dataComplexity: DataComplexity,
  timeToMarket: TimeToMarket,
  specialConstraints: z.array(z.string()).optional(),
});

export type Requirements = z.infer<typeof RequirementsSchema>;
