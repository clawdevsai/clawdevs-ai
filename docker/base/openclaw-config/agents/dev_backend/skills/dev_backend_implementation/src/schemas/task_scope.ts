import { z } from 'zod';

/**
 * TaskComplexity enum - Defines the complexity level of a task
 * - simple: Basic CRUD or straightforward implementation
 * - moderate: Some complexity, a few moving parts
 * - complex: Multiple components, architectural decisions needed
 * - extreme: Highly complex, advanced patterns required
 */
export const TaskComplexity = z.enum(['simple', 'moderate', 'complex', 'extreme']);
export type TaskComplexity = z.infer<typeof TaskComplexity>;

/**
 * TaskScopeSchema - Defines the scope and constraints of a development task
 *
 * Used to understand:
 * - What the task is trying to accomplish
 * - How long it should take
 * - What quality gates should be enforced
 * - Whether specialized reviews are needed
 */
export const TaskScopeSchema = z.object({
  /** Human-readable title of the task */
  title: z.string().min(1, 'Task title is required').max(200, 'Task title too long'),

  /** Detailed description of what needs to be implemented */
  description: z
    .string()
    .min(10, 'Description should be at least 10 characters')
    .max(2000, 'Description is too long'),

  /** Estimated number of days to complete (0.5 = half day, 5 = full week) */
  estimatedDays: z
    .number()
    .positive('Estimated days must be positive')
    .max(30, 'Task too large, consider breaking down'),

  /** Whether this task requires security review (auth, crypto, secrets) */
  requiresSecurityReview: z.boolean().default(false),

  /** Whether this task requires performance review (optimization, benchmarks) */
  requiresPerformanceReview: z.boolean().default(false),

  /** Overall complexity of the task */
  complexity: TaskComplexity,

  /** Optional: Special constraints or considerations */
  specialConstraints: z.array(z.string()).optional(),

  /** Optional: Related tasks or dependencies */
  dependencies: z.array(z.string()).optional(),

  /** Optional: Success criteria for the task */
  successCriteria: z.array(z.string()).optional(),
});

export type TaskScope = z.infer<typeof TaskScopeSchema>;

/**
 * validateTaskScope - Validates and parses a task scope object
 *
 * @param input The input object to validate
 * @returns Validated TaskScope object or throws ZodError
 *
 * @example
 * ```typescript
 * const scope = validateTaskScope({
 *   title: 'Implement caching layer',
 *   description: 'Add Redis caching for frequently accessed data',
 *   estimatedDays: 2,
 *   requiresPerformanceReview: true,
 *   complexity: 'moderate'
 * });
 * ```
 */
export function validateTaskScope(input: unknown): TaskScope {
  return TaskScopeSchema.parse(input);
}

/**
 * isHighRisk - Determines if a task scope indicates high-risk work
 *
 * High-risk tasks:
 * - Require security review
 * - Have extreme complexity
 * - Touch critical infrastructure
 * - Have security/performance requirements
 *
 * @param scope The task scope to evaluate
 * @returns true if the task is considered high-risk
 */
export function isHighRisk(scope: TaskScope): boolean {
  return (
    scope.requiresSecurityReview ||
    scope.requiresPerformanceReview ||
    scope.complexity === 'extreme' ||
    (scope.specialConstraints && scope.specialConstraints.some((c) => c.toLowerCase().includes('security')))
  );
}

/**
 * estimateEffort - Provides effort estimation in different units
 *
 * Converts estimatedDays into more human-friendly formats
 *
 * @param scope The task scope
 * @returns Object with different time estimates
 */
export function estimateEffort(scope: TaskScope) {
  const days = scope.estimatedDays;
  const hours = days * 8;
  const weeks = days / 5;

  return {
    days: days.toFixed(1),
    hours: Math.round(hours),
    weeks: weeks.toFixed(1),
    workDaysTeamNeeds: Math.ceil(days),
    humanReadable: formatEffort(days),
  };
}

/**
 * formatEffort - Formats effort estimate as human-readable string
 *
 * @param days The number of days
 * @returns Human-readable effort string
 */
function formatEffort(days: number): string {
  if (days < 1) {
    return `${Math.round(days * 8)} hours`;
  } else if (days < 5) {
    return `${days.toFixed(1)} days`;
  } else if (days < 20) {
    return `${(days / 5).toFixed(1)} weeks`;
  } else {
    return `${(days / 20).toFixed(1)} months`;
  }
}

/**
 * getRecommendedApproach - Recommends a development approach based on task scope
 *
 * Suggests:
 * - Test-driven development for complex tasks
 * - Pair programming for high-risk tasks
 * - Architecture review for extreme complexity
 *
 * @param scope The task scope
 * @returns Array of recommended practices
 */
export function getRecommendedApproach(scope: TaskScope): string[] {
  const recommendations: string[] = [];

  // Test-driven approach
  if (scope.complexity === 'complex' || scope.complexity === 'extreme') {
    recommendations.push('Use Test-Driven Development (TDD)');
    recommendations.push('Start with comprehensive test cases before implementation');
  }

  // Security review
  if (scope.requiresSecurityReview) {
    recommendations.push('Have code reviewed by security specialist');
    recommendations.push('Run security linting and vulnerability checks');
    recommendations.push('Document all security decisions');
  }

  // Performance review
  if (scope.requiresPerformanceReview) {
    recommendations.push('Benchmark before and after optimization');
    recommendations.push('Profile with production-like load');
    recommendations.push('Document performance characteristics');
  }

  // Pair programming for high risk
  if (isHighRisk(scope) && scope.estimatedDays < 5) {
    recommendations.push('Consider pair programming with senior developer');
  }

  // Architecture review for extreme
  if (scope.complexity === 'extreme') {
    recommendations.push('Conduct architecture review with team leads');
    recommendations.push('Document decision rationale');
    recommendations.push('Plan for iterative refinement');
  }

  // High test coverage for all
  recommendations.push('Maintain minimum 80% code coverage');
  recommendations.push('Include integration tests for critical paths');

  return recommendations;
}
