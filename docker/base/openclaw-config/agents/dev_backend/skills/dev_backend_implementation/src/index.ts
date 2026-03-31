/**
 * dev_backend_implementation - Intelligent skill for backend implementation
 *
 * Analyzes requirements and recommends optimal technology stacks
 * through an intelligent hook system.
 *
 * Main exports:
 * - beforeExecution: Hook that analyzes requirements and recommends tech stack
 * - Schemas: Requirements, Recommendations, TaskScope validation
 * - Utilities: Requirement parsing, logging
 * - Decisions: Architecture patterns and recommendations
 */

// Export main hooks
export { beforeExecution } from './hooks/before_execution';
export type { ExecutionContext, ExecutionResult } from './hooks/before_execution';

// Export schemas
export { RequirementsSchema, type Requirements } from './schemas/requirements';
export type {
  VolumeRequirement,
  LatencyRequirement,
  CostSensitivity,
  Reliability,
  DataComplexity,
  TimeToMarket,
} from './schemas/requirements';

export { RecommendationSchema, type Recommendation } from './schemas/recommendations';
export type {
  LanguageRecommendation,
  ProtocolRecommendation,
  DatabaseRecommendation,
  ArchitecturalPattern,
  MessagingRecommendation,
  Tradeoff,
  Alternative,
} from './schemas/recommendations';

export { TaskScopeSchema, validateTaskScope, isHighRisk, estimateEffort, getRecommendedApproach } from './schemas/task_scope';
export type { TaskScope, TaskComplexity } from './schemas/task_scope';

// Export decision/recommendation utilities
export { getRecommendation, getAllPatterns, getPatternByName, comparePatterns, getPatternsByRequirement } from './decisions/recommendations';
export { findMatchingPattern, ARCHITECTURE_PATTERNS } from './decisions/architecture_matrix';
export type { ArchitecturePattern } from './decisions/architecture_matrix';

export { getPattern, getAllPatternNames, getPatternDescription, getPatternsForUseCase } from './decisions/patterns';
export type { PatternGuide } from './decisions/patterns';

// Export utilities
export { logger } from './utils/logger';
export { requirementParser } from './utils/requirement-parser';
export type { RequirementSource } from './utils/requirement-parser';

/**
 * Skill configuration metadata
 *
 * This object provides metadata about the skill for the framework:
 * - name: Unique identifier for the skill
 * - version: Semantic version for tracking changes
 * - description: Human-readable description
 * - hooks: Lifecycle hooks provided by this skill
 *
 * The hooks are the integration points where this skill is invoked:
 * - beforeExecution: Called before each skill execution to analyze requirements
 * - (afterExecution: For future implementation)
 */
export const skillConfig = {
  name: 'dev_backend_implementation',
  version: '2.0.0',
  description: 'Intelligent backend implementation skill with requirement analysis and tech stack recommendations',

  hooks: {
    beforeExecution: {
      enabled: true,
      description: 'Analyzes requirements from conversation/config/system prompt and recommends optimal tech stack',
    },
  },

  patterns: {
    supported: [
      'High Performance',
      'Low Cost',
      'High Reliability',
      'MVP/Quick Launch',
      'Standard Web Application',
      'Real-Time Data Processing',
    ],
    count: 6,
  },

  technologies: {
    languages: ['go', 'rust', 'typescript', 'python', 'java', 'csharp'],
    protocols: ['grpc', 'rest', 'websocket', 'graphql', 'mqtt'],
    databases: ['postgresql', 'mysql', 'mongodb', 'dynamodb', 'cassandra', 'redis', 'elasticsearch'],
    patterns: ['monolith', 'microservices', 'serverless', 'event_driven', 'batch', 'streaming', 'distributed'],
    messaging: ['kafka', 'rabbitmq', 'sqs', 'pubsub'],
  },
};

export default skillConfig;
