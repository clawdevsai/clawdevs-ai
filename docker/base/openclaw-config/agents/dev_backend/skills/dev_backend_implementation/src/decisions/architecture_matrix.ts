/**
 * Architecture Decision Matrix
 *
 * Maps requirements (performance, reliability, cost) to tech stack recommendations.
 * Used by beforeExecution hook to guide implementation decisions.
 *
 * Will be fully implemented in Task 2.3 with:
 * - Scoring algorithm
 * - Pattern matching
 * - Trade-off analysis
 */

export const ARCHITECTURE_MATRIX = [
  {
    name: 'High Performance',
    volume: 'extreme',
    latency: 'realtime',
    language: 'Go',
    protocol: 'gRPC',
    database: 'Redis + PostgreSQL',
    cache: 'Redis/Memcached',
    messaging: 'Kafka/RabbitMQ',
    deployment: 'Kubernetes',
    minServers: 5,
    estimatedCost: 'High',
  },
  {
    name: 'Standard Web',
    volume: 'moderate',
    latency: '200-500ms',
    language: 'Node.js / Python',
    protocol: 'REST/GraphQL',
    database: 'PostgreSQL',
    cache: 'Redis',
    messaging: 'Bull/Celery',
    deployment: 'Docker + Load Balancer',
    minServers: 2,
    estimatedCost: 'Medium',
  },
  {
    name: 'Low Cost MVP',
    volume: 'low',
    latency: '1-2s',
    language: 'Node.js / Python',
    protocol: 'REST',
    database: 'PostgreSQL / SQLite',
    cache: 'In-memory',
    messaging: 'Basic queues',
    deployment: 'Single server',
    minServers: 1,
    estimatedCost: 'Low',
  },
  {
    name: 'High Reliability',
    volume: 'high',
    latency: '50-200ms',
    language: 'Go / Java',
    protocol: 'gRPC',
    database: 'PostgreSQL (replicated)',
    cache: 'Redis (replicated)',
    messaging: 'Kafka (multi-broker)',
    deployment: 'Kubernetes multi-region',
    minServers: 10,
    estimatedCost: 'Very High',
  },
];
