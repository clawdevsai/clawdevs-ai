import { z } from 'zod';

/**
 * Language enum - Primary programming language for implementation
 */
export const LanguageRecommendation = z.enum(['go', 'rust', 'typescript', 'python', 'java', 'csharp']);
export type LanguageRecommendation = z.infer<typeof LanguageRecommendation>;

/**
 * Protocol enum - Communication protocol between services
 */
export const ProtocolRecommendation = z.enum(['grpc', 'rest', 'websocket', 'graphql', 'mqtt']);
export type ProtocolRecommendation = z.infer<typeof ProtocolRecommendation>;

/**
 * Database enum - Primary data store
 */
export const DatabaseRecommendation = z.union([
  z.enum(['postgresql', 'mysql', 'mongodb', 'dynamodb', 'cassandra', 'redis', 'elasticsearch']),
  z.string(),
]);
export type DatabaseRecommendation = z.infer<typeof DatabaseRecommendation>;

/**
 * Pattern enum - Architectural pattern for system design
 */
export const ArchitecturalPattern = z.enum([
  'monolith',
  'microservices',
  'serverless',
  'event_driven',
  'batch',
  'streaming',
  'distributed',
]);
export type ArchitecturalPattern = z.infer<typeof ArchitecturalPattern>;

/**
 * Messaging enum - Message broker/queue technology
 */
export const MessagingRecommendation = z.enum(['kafka', 'rabbitmq', 'sqs', 'pubsub', 'none']);
export type MessagingRecommendation = z.infer<typeof MessagingRecommendation>;

/**
 * Tradeoff - Evaluation of implementation tradeoffs
 */
export const Tradeoff = z.object({
  performance: z.union([z.number().min(0).max(100), z.string()]),
  development_speed: z.union([z.number().min(0).max(100), z.string()]),
  operational_complexity: z.union([z.number().min(0).max(100), z.string()]),
  cost_efficiency: z.union([z.number().min(0).max(100), z.string()]),
});
export type Tradeoff = z.infer<typeof Tradeoff>;

/**
 * Alternative - Alternative technology or approach
 */
export const Alternative = z.object({
  language: z.string(),
  pros: z.array(z.string()),
  cons: z.array(z.string()),
});
export type Alternative = z.infer<typeof Alternative>;

/**
 * RecommendationSchema - Defines all recommended technologies and patterns
 */
export const RecommendationSchema = z.object({
  language: LanguageRecommendation,
  protocol: ProtocolRecommendation,
  database: DatabaseRecommendation,
  pattern: ArchitecturalPattern,
  messaging: MessagingRecommendation,
  reasoning: z.string(),
  tradeoffs: Tradeoff,
  alternatives: z.array(Alternative).optional(),
});

export type Recommendation = z.infer<typeof RecommendationSchema>;
