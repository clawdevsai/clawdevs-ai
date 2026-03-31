/**
 * Shared schemas for all dev_backend skills
 * Defines types and validation rules for requirements and recommendations
 */

export {
  VolumeRequirement,
  LatencyRequirement,
  CostSensitivity,
  Reliability,
  DataComplexity,
  TimeToMarket,
  RequirementsSchema,
  type Requirements,
} from './requirements';

export {
  LanguageRecommendation,
  ProtocolRecommendation,
  DatabaseRecommendation,
  ArchitecturalPattern,
  MessagingRecommendation,
  Tradeoff,
  Alternative,
  RecommendationSchema,
  type Recommendation,
} from './recommendations';
