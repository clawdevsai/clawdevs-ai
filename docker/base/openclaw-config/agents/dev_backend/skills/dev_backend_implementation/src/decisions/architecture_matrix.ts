import { Requirements } from '../schemas/requirements';
import { Recommendation } from '../schemas/recommendations';

/**
 * ArchitecturePattern - Represents a complete architecture decision pattern
 * Maps requirements to recommended technology stack with detailed analysis
 */
export interface ArchitecturePattern {
  /** Unique identifier for this pattern */
  name: string;

  /** Human-readable description of what this pattern is optimized for */
  description: string;

  /** Requirements that match this pattern */
  requirements: {
    volume?: string[];
    latency?: string[];
    costSensitivity?: string[];
    reliability?: string[];
    dataComplexity?: string[];
    timeToMarket?: string[];
  };

  /** The recommendation object (without reasoning field) */
  recommendation: Omit<Recommendation, 'reasoning' | 'tradeoffs' | 'alternatives'>;

  /** Detailed reasoning for why this pattern fits */
  reasoning: string;

  /** Trade-off analysis for this pattern */
  tradeoffs: {
    performance: string;
    development_speed: string;
    operational_complexity: string;
    cost_efficiency: string;
  };

  /** Alternative approaches with pros and cons */
  alternatives?: Array<{
    language: string;
    pros: string[];
    cons: string[];
  }>;
}

/**
 * ARCHITECTURE_PATTERNS - Repository of real-world architecture patterns
 * Each pattern maps specific requirements to optimal tech stack choices
 *
 * Patterns included:
 * 1. High Performance: For 1M+ req/s with <100ms latency
 * 2. Low Cost: For startups with limited budgets
 * 3. High Reliability: For mission-critical systems (99.99% uptime)
 * 4. MVP/Quick Launch: For rapid prototyping and 2-week launches
 */
export const ARCHITECTURE_PATTERNS: ArchitecturePattern[] = [
  {
    name: 'High Performance',
    description: 'For 1M+ req/s with <100ms latency and extreme scale',
    requirements: {
      volume: ['extreme'],
      latency: ['realtime', 'ultra'],
      reliability: ['critical', 'highly_critical'],
    },
    recommendation: {
      language: 'go',
      protocol: 'grpc',
      database: 'PostgreSQL + Redis',
      pattern: 'microservices',
      messaging: 'kafka',
    },
    reasoning:
      'Go offers excellent concurrency primitives (goroutines) and produces single binary deployments with low memory overhead. gRPC provides efficient binary protocol with HTTP/2 multiplexing, enabling 1M+ req/s. Redis for hot data caching with sub-millisecond access. Kafka for durable, distributed event processing at scale. Microservices pattern allows independent scaling of components based on load.',
    tradeoffs: {
      performance: 'Excellent (optimized for 1M+ req/s, <100ms p99)',
      development_speed: 'Medium (Go learning curve, but strong tooling)',
      operational_complexity: 'High (distributed systems, service mesh, monitoring)',
      cost_efficiency: 'Good (efficient resource usage, but infrastructure costs)',
    },
    alternatives: [
      {
        language: 'rust',
        pros: ['Even better performance', 'Memory safety without GC', 'Fine-grained control'],
        cons: ['Significantly steeper learning curve', 'Slower development velocity', 'Complex async ecosystem'],
      },
      {
        language: 'java',
        pros: ['Mature ecosystem', 'Strong concurrency libraries', 'Excellent JVM performance'],
        cons: ['Higher memory usage (JVM overhead)', 'Slower startup times', 'More verbose'],
      },
    ],
  },

  {
    name: 'Low Cost',
    description: 'For startups and cost-sensitive projects with limited budgets',
    requirements: {
      volume: ['low', 'medium'],
      latency: ['normal', 'responsive'],
      costSensitivity: ['high'],
    },
    recommendation: {
      language: 'typescript',
      protocol: 'rest',
      database: 'SQLite',
      pattern: 'serverless',
      messaging: 'none',
    },
    reasoning:
      'TypeScript with Node.js enables rapid development with fast iteration cycles and immediate feedback. Serverless (AWS Lambda, Google Cloud Run) eliminates server management, scales automatically, and charges only for actual usage. SQLite provides zero-cost database with excellent local development experience. REST keeps implementation simple and widely understood. Minimal infrastructure reduces operational burden and costs to $30-100/month.',
    tradeoffs: {
      performance: 'Good (adequate for medium volume, not optimized)',
      development_speed: 'Excellent (rapid prototyping, quick iterations)',
      operational_complexity: 'Low (serverless handles scaling and monitoring)',
      cost_efficiency: 'Excellent ($30-100/month, scales with usage)',
    },
    alternatives: [
      {
        language: 'python',
        pros: ['Rapid development', 'Excellent data libraries', 'Great for scripting'],
        cons: ['Slower runtime performance', 'Higher memory usage', 'Python startup overhead'],
      },
      {
        language: 'go',
        pros: ['Better performance than Python', 'Single binary', 'Good concurrency'],
        cons: ['Slightly longer development time', 'Less ecosystem for rapid dev'],
      },
    ],
  },

  {
    name: 'High Reliability',
    description: 'For mission-critical systems requiring 99.99% uptime and failover',
    requirements: {
      reliability: ['highly_critical'],
      volume: ['high', 'extreme'],
    },
    recommendation: {
      language: 'go',
      protocol: 'grpc',
      database: 'PostgreSQL + replicas',
      pattern: 'distributed',
      messaging: 'kafka',
    },
    reasoning:
      'Go for production reliability and performance. Distributed pattern enables fault isolation and graceful degradation. PostgreSQL with synchronous replication and hot standby ensures zero data loss and automatic failover. Kafka for durable, replicated message processing with exactly-once semantics. Multi-region deployment with health checks and automated failover achieves 99.99% SLA. Circuit breakers and bulkheads prevent cascade failures.',
    tradeoffs: {
      performance: 'Excellent (optimized for high throughput)',
      development_speed: 'Medium (distributed complexity)',
      operational_complexity: 'Very High (multi-region, database replication, monitoring)',
      cost_efficiency: 'Medium (requires redundant infrastructure, $5k+/month)',
    },
    alternatives: [
      {
        language: 'rust',
        pros: ['Memory safety', 'Fine-grained performance control', 'No GC pauses'],
        cons: ['Steep learning curve', 'Slower development'],
      },
      {
        language: 'java',
        pros: ['Mature frameworks', 'Strong ecosystem', 'Proven at scale'],
        cons: ['JVM startup overhead', 'Higher memory usage', 'More verbose'],
      },
    ],
  },

  {
    name: 'MVP/Quick Launch',
    description: 'For 2-4 week MVP launches and rapid prototyping',
    requirements: {
      timeToMarket: ['asap'],
      volume: ['low'],
      costSensitivity: ['high', 'medium'],
    },
    recommendation: {
      language: 'typescript',
      protocol: 'rest',
      database: 'SQLite',
      pattern: 'monolith',
      messaging: 'none',
    },
    reasoning:
      'TypeScript + Express maximizes developer velocity with full-stack JavaScript and immediate feedback. Monolith architecture eliminates distributed systems complexity and keeps deployment straightforward. SQLite requires zero setup and works perfectly for MVP with single-instance deployment. REST API is simple to implement and easy to test. Everything runs on single server with minimal operational overhead. Can evolve to microservices after validation.',
    tradeoffs: {
      performance: 'Adequate (sufficient for MVP validation)',
      development_speed: 'Excellent (fastest time to market)',
      operational_complexity: 'Minimal (single process, simple deployment)',
      cost_efficiency: 'Excellent ($0-20/month, can run on free tier)',
    },
    alternatives: [
      {
        language: 'python',
        pros: ['Very rapid development', 'Great for data work', 'Flask/Django mature'],
        cons: ['Slower runtime', 'Higher memory overhead'],
      },
      {
        language: 'go',
        pros: ['Better performance', 'Single binary', 'Simple deployment'],
        cons: ['Slightly more code', 'Less ecosystem for web'],
      },
    ],
  },

  {
    name: 'Standard Web Application',
    description: 'For typical web applications with moderate scale (medium volume, normal latency)',
    requirements: {
      volume: ['medium'],
      latency: ['normal', 'responsive'],
    },
    recommendation: {
      language: 'typescript',
      protocol: 'rest',
      database: 'postgresql',
      pattern: 'monolith',
      messaging: 'none',
    },
    reasoning:
      'TypeScript with Express or Fastify provides excellent developer experience with type safety. Monolith architecture is straightforward to develop and deploy. PostgreSQL is battle-tested, reliable, and has rich features for typical web applications. REST is widely understood and sufficient for most use cases. Single deployment unit simplifies operations while having room to scale vertically or horizontally if needed.',
    tradeoffs: {
      performance: 'Good (sufficient for medium volume)',
      development_speed: 'Excellent (rapid development)',
      operational_complexity: 'Low-Medium (single application, standard database)',
      cost_efficiency: 'Good ($100-500/month depending on scale)',
    },
    alternatives: [
      {
        language: 'python',
        pros: ['Rapid development', 'Django has batteries included', 'Great ORM'],
        cons: ['Performance ceiling at scale', 'Higher memory usage'],
      },
      {
        language: 'go',
        pros: ['Better performance', 'Simpler deployment', 'Excellent concurrency'],
        cons: ['More verbose than Python/Node', 'Smaller web ecosystem'],
      },
    ],
  },

  {
    name: 'Real-Time Data Processing',
    description: 'For systems requiring streaming data, complex analytics, or real-time updates',
    requirements: {
      dataComplexity: ['extreme'],
      latency: ['responsive', 'realtime'],
    },
    recommendation: {
      language: 'go',
      protocol: 'websocket',
      database: 'PostgreSQL + TimescaleDB',
      pattern: 'event_driven',
      messaging: 'kafka',
    },
    reasoning:
      'Go excels at handling concurrent connections with goroutines. WebSocket enables real-time bidirectional communication with clients. Kafka provides high-throughput event streaming with ordering guarantees. TimescaleDB (PostgreSQL extension) optimizes for time-series data with excellent query performance. Event-driven pattern allows systems to react immediately to data changes. Suitable for dashboards, notifications, and complex real-time analytics.',
    tradeoffs: {
      performance: 'Excellent (optimized for concurrent connections)',
      development_speed: 'Medium (event-driven complexity)',
      operational_complexity: 'Medium-High (Kafka, real-time pipeline)',
      cost_efficiency: 'Good-Medium (depends on volume, typically $1k-5k/month)',
    },
    alternatives: [
      {
        language: 'rust',
        pros: ['Highest performance', 'Memory safety', 'No GC pauses'],
        cons: ['Longer development time', 'Steeper learning curve'],
      },
      {
        language: 'java',
        pros: ['Rich data processing libraries', 'Spring ecosystem', 'Mature tools'],
        cons: ['Higher memory usage', 'JVM overhead', 'More verbose'],
      },
    ],
  },
];

/**
 * findMatchingPattern - Scores all patterns against requirements and returns best match
 *
 * Scoring algorithm:
 * - Each requirement match adds 3 points
 * - Missing requirement match adds 0 points
 * - Pattern accepting any value adds 1 point
 * - Returns pattern with highest score
 *
 * @param requirements The requirements object to match against
 * @returns The best matching pattern, or null if no pattern can be found
 */
export function findMatchingPattern(requirements: Requirements): ArchitecturePattern | null {
  let bestMatch: ArchitecturePattern | null = null;
  let bestScore = 0;

  for (const pattern of ARCHITECTURE_PATTERNS) {
    let score = 0;

    // Score volume match
    if (pattern.requirements.volume?.includes(requirements.volume)) {
      score += 3;
    } else if (pattern.requirements.volume && pattern.requirements.volume.length > 0) {
      score += 0;
    } else {
      score += 1; // Pattern accepts any volume
    }

    // Score latency match
    if (pattern.requirements.latency?.includes(requirements.latency)) {
      score += 3;
    } else if (pattern.requirements.latency && pattern.requirements.latency.length > 0) {
      score += 0;
    } else {
      score += 1;
    }

    // Score cost match
    if (pattern.requirements.costSensitivity?.includes(requirements.costSensitivity)) {
      score += 2;
    } else if (pattern.requirements.costSensitivity && pattern.requirements.costSensitivity.length > 0) {
      score += 0;
    } else {
      score += 1;
    }

    // Score reliability match
    if (pattern.requirements.reliability?.includes(requirements.reliability)) {
      score += 2;
    } else if (pattern.requirements.reliability && pattern.requirements.reliability.length > 0) {
      score += 0;
    } else {
      score += 1;
    }

    // Score data complexity match
    if (pattern.requirements.dataComplexity?.includes(requirements.dataComplexity)) {
      score += 2;
    } else if (pattern.requirements.dataComplexity && pattern.requirements.dataComplexity.length > 0) {
      score += 0;
    } else {
      score += 1;
    }

    // Score time to market match
    if (pattern.requirements.timeToMarket?.includes(requirements.timeToMarket)) {
      score += 2;
    } else if (pattern.requirements.timeToMarket && pattern.requirements.timeToMarket.length > 0) {
      score += 0;
    } else {
      score += 1;
    }

    if (score > bestScore) {
      bestScore = score;
      bestMatch = pattern;
    }
  }

  return bestMatch;
}
