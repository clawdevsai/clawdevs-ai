import { z } from "zod";

/**
 * Architecture Pattern Interface
 * Defines a complete frontend architecture pattern with technology stack,
 * scoring criteria, trade-offs, and alternatives
 */
export interface ArchitecturePattern {
  id: string;
  name: string;
  description: string;

  // Technology Stack
  framework: string;
  language: string;
  buildTool: string;
  styling: string;
  stateManagement: string;
  testing: string;

  // Scoring Criteria
  scoringFactors: {
    volume: number; // 0-100 (higher is better for large projects)
    latency: number; // 0-100 (higher is better for performance)
    costSensitivity: number; // 0-100 (higher means better for budget-conscious)
    reliability: number; // 0-100 (higher for mission-critical)
    uiComplexity: number; // 0-100 (higher for complex UIs)
    timeToMarket: number; // 0-100 (higher for quick launch)
  };

  // Characteristics
  characteristics: {
    bundleSize: "tiny" | "small" | "medium" | "large";
    buildTime: "instant" | "fast" | "moderate" | "slow";
    devExperience: "excellent" | "good" | "fair" | "poor";
    scalability: "limited" | "good" | "excellent" | "unlimited";
    maintenance: "low" | "moderate" | "high" | "very_high";
    seoCapability: "excellent" | "good" | "fair" | "poor";
    mobileFirst: boolean;
    progressiveEnhancement: boolean;
  };

  // Cost Estimation
  costEstimate: {
    infrastructure: string; // e.g., "$100-500/month"
    development: string; // e.g., "3-8 weeks"
    maintenance: string; // e.g., "$500-1k/month"
  };

  // Business Alignment
  reasoning: string;
  bestFor: string[];
  teamSize: string;
  scalableTo: string;

  // Decision Support
  tradeoffs: {
    advantages: string[];
    disadvantages: string[];
  };

  alternatives: string[];
  migration: {
    from: string[];
    difficulty: "easy" | "moderate" | "hard" | "very_hard";
  };
}

/**
 * Frontend Architecture Matrix
 * Contains all supported frontend architecture patterns
 */
export const architecturePatterns: ArchitecturePattern[] = [
  {
    id: "component_driven",
    name: "Component-Driven Architecture",
    description:
      "Structured component library approach with design system and strong type safety",

    framework: "React/Vue/Angular",
    language: "TypeScript",
    buildTool: "Vite/Webpack",
    styling: "CSS Modules/Tailwind",
    stateManagement: "Redux/Pinia/Context",
    testing: "Vitest/Jest/Testing Library",

    scoringFactors: {
      volume: 95, // Excellent for large projects
      latency: 70, // Client-side rendering has latency
      costSensitivity: 40, // Higher setup costs
      reliability: 85, // Good with proper patterns
      uiComplexity: 95, // Excellent for complex UIs
      timeToMarket: 60, // Moderate setup time
    },

    characteristics: {
      bundleSize: "medium",
      buildTime: "fast",
      devExperience: "excellent",
      scalability: "excellent",
      maintenance: "low",
      seoCapability: "fair",
      mobileFirst: true,
      progressiveEnhancement: false,
    },

    costEstimate: {
      infrastructure: "$2k-5k/month",
      development: "4-8 weeks",
      maintenance: "$2k-4k/month",
    },

    reasoning:
      "Provides excellent component reusability, strong type safety, and design consistency. Ideal for teams that want to scale to 50k+ LOC with 10+ developers.",

    bestFor: [
      "Complex interactive UIs",
      "Design systems",
      "Large teams (10+ devs)",
      "Long-term maintenance",
      "Enterprise applications",
      "SaaS platforms",
    ],

    teamSize: "10-50 developers",
    scalableTo: "500k+ LOC",

    tradeoffs: {
      advantages: [
        "Excellent component reusability",
        "Strong type safety with TypeScript",
        "Mature ecosystem and tooling",
        "Design consistency across app",
        "Good testing infrastructure",
        "Mobile-responsive components",
        "Excellent documentation",
      ],
      disadvantages: [
        "Larger bundle size than alternatives",
        "Steeper learning curve",
        "More setup complexity",
        "Client-side rendering latency",
        "SEO requires extra work",
        "Higher initial setup cost",
      ],
    },

    alternatives: [
      "progressive_enhancement",
      "micro_frontend",
      "lightweight_spa",
    ],

    migration: {
      from: ["fullstack_monolith", "lightweight_spa"],
      difficulty: "moderate",
    },
  },

  {
    id: "progressive_enhancement",
    name: "Progressive Enhancement (SSR + Islands)",
    description:
      "Server-side rendering with selective client hydration for optimal performance",

    framework: "Next.js/Nuxt/Remix",
    language: "TypeScript",
    buildTool: "Webpack/Turbopack",
    styling: "Tailwind/CSS Modules",
    stateManagement: "React Context/Vue Pinia",
    testing: "Playwright/Vitest",

    scoringFactors: {
      volume: 90, // Very good for large projects
      latency: 95, // Excellent performance (SSR)
      costSensitivity: 70, // Lower cost than CSR
      reliability: 90, // High reliability
      uiComplexity: 80, // Good for most UIs
      timeToMarket: 75, // Fast setup
    },

    characteristics: {
      bundleSize: "small",
      buildTime: "fast",
      devExperience: "excellent",
      scalability: "excellent",
      maintenance: "very_high",
      seoCapability: "excellent",
      mobileFirst: true,
      progressiveEnhancement: true,
    },

    costEstimate: {
      infrastructure: "$500-2k/month",
      development: "2-4 weeks",
      maintenance: "$1k-2k/month",
    },

    reasoning:
      "Combines the best of both worlds: fast initial page load (SSR) with interactive UI (hydration). Perfect for content-heavy sites and e-commerce.",

    bestFor: [
      "E-commerce platforms",
      "Content-heavy sites",
      "SEO-critical applications",
      "Mobile web apps",
      "High-traffic sites",
      "Blogs and documentation",
    ],

    teamSize: "5-20 developers",
    scalableTo: "200k+ LOC",

    tradeoffs: {
      advantages: [
        "Excellent SEO performance",
        "Fast First Contentful Paint (FCP)",
        "Reduced client-side JavaScript",
        "Server can render dynamic content",
        "Progressive enhancement built-in",
        "Good developer experience",
        "Edge computing support",
      ],
      disadvantages: [
        "More complex hydration logic",
        "Requires server infrastructure",
        "Harder to debug state mismatches",
        "Data fetching complexity",
        "Dual-environment development",
      ],
    },

    alternatives: ["component_driven", "headless_cms", "lightweight_spa"],

    migration: {
      from: ["component_driven", "lightweight_spa"],
      difficulty: "moderate",
    },
  },

  {
    id: "micro_frontend",
    name: "Micro-Frontend Architecture",
    description:
      "Independent deployable teams with module federation and shared dependencies",

    framework: "React/Vue (Module Federation)",
    language: "TypeScript",
    buildTool: "Webpack (Module Federation)",
    styling: "Design Tokens/CSS-in-JS",
    stateManagement: "Redux/Zustand (shared)",
    testing: "Jest/Vitest + E2E tests",

    scoringFactors: {
      volume: 100, // Perfect for massive projects
      latency: 65, // Network overhead from federation
      costSensitivity: 30, // High infrastructure cost
      reliability: 80, // Good with proper governance
      uiComplexity: 85, // Good for complex orgs
      timeToMarket: 50, // Complex setup
    },

    characteristics: {
      bundleSize: "large",
      buildTime: "moderate",
      devExperience: "good",
      scalability: "unlimited",
      maintenance: "high",
      seoCapability: "fair",
      mobileFirst: true,
      progressiveEnhancement: false,
    },

    costEstimate: {
      infrastructure: "$5k-10k/month",
      development: "6-12 weeks",
      maintenance: "$4k-8k/month",
    },

    reasoning:
      "Enables independent team deployment and scalable org structure. Essential for 100k+ LOC with 20+ teams.",

    bestFor: [
      "Large organizations",
      "Independent teams",
      "Legacy system integration",
      "Decoupled domain ownership",
      "Multi-product platforms",
    ],

    teamSize: "20-100 developers",
    scalableTo: "1M+ LOC",

    tradeoffs: {
      advantages: [
        "Independent team velocity",
        "Domain isolation",
        "Scalable org structure",
        "Gradual upgrades per team",
        "Shared infrastructure",
        "Reduced coordination overhead",
      ],
      disadvantages: [
        "Complex build and deployment",
        "Runtime complexity and debugging",
        "Shared dependency management",
        "Network overhead",
        "Larger bundle sizes",
        "Requires clear governance",
      ],
    },

    alternatives: ["component_driven", "progressive_enhancement"],

    migration: {
      from: ["component_driven"],
      difficulty: "hard",
    },
  },

  {
    id: "lightweight_spa",
    name: "Lightweight SPA (Vanilla/Preact)",
    description:
      "Minimal dependencies, fast load times, ideal for MVPs and performance-critical apps",

    framework: "Vanilla JS/Preact/Alpine",
    language: "JavaScript/TypeScript",
    buildTool: "Vite/esbuild",
    styling: "Tailwind/Vanilla CSS",
    stateManagement: "Zustand/Nano Stores",
    testing: "Vitest/uvu",

    scoringFactors: {
      volume: 50, // Limited for large projects
      latency: 98, // Excellent performance
      costSensitivity: 95, // Minimal costs
      reliability: 75, // Good with discipline
      uiComplexity: 40, // Limited for complex UIs
      timeToMarket: 95, // Very fast launch
    },

    characteristics: {
      bundleSize: "tiny",
      buildTime: "instant",
      devExperience: "good",
      scalability: "limited",
      maintenance: "fair",
      seoCapability: "fair",
      mobileFirst: true,
      progressiveEnhancement: true,
    },

    costEstimate: {
      infrastructure: "$0-500/month",
      development: "1-2 weeks",
      maintenance: "$0-500/month",
    },

    reasoning:
      "Perfect for startups, MVPs, and performance-critical applications. Get to market in 1-2 weeks with minimal overhead.",

    bestFor: [
      "Startups and MVPs",
      "Performance-critical apps",
      "Simple interactive needs",
      "Proof-of-concept projects",
      "Admin dashboards",
      "Low-resource deployments",
    ],

    teamSize: "1-5 developers",
    scalableTo: "20k LOC",

    tradeoffs: {
      advantages: [
        "Minimal dependencies",
        "Fastest load time",
        "Tiny bundle size",
        "Quick launch",
        "Easy to understand code",
        "Low maintenance overhead",
        "Bootstrap-friendly",
      ],
      disadvantages: [
        "Limited scaling potential",
        "Fewer framework features",
        "Less ecosystem support",
        "Manual state management",
        "Harder to structure large apps",
        "Less developer tooling",
      ],
    },

    alternatives: ["progressive_enhancement", "component_driven"],

    migration: {
      from: [],
      difficulty: "easy",
    },
  },

  {
    id: "headless_cms",
    name: "Headless CMS + Static Generation",
    description:
      "Content-first approach with static HTML generation for ultimate performance",

    framework: "11ty/Hugo/Astro",
    language: "JavaScript/Markdown",
    buildTool: "11ty/Astro",
    styling: "Tailwind/Vanilla CSS",
    stateManagement: "None (static)",
    testing: "Playwright",

    scoringFactors: {
      volume: 70, // Good for content sites
      latency: 100, // Perfect performance
      costSensitivity: 90, // Very low cost
      reliability: 100, // Extremely reliable
      uiComplexity: 30, // Limited for interactive
      timeToMarket: 85, // Fast build
    },

    characteristics: {
      bundleSize: "tiny",
      buildTime: "moderate",
      devExperience: "excellent",
      scalability: "excellent",
      maintenance: "very_high",
      seoCapability: "excellent",
      mobileFirst: true,
      progressiveEnhancement: true,
    },

    costEstimate: {
      infrastructure: "$100-1k/month",
      development: "1-3 weeks",
      maintenance: "$200-500/month",
    },

    reasoning:
      "Best performance possible with unlimited scalability. Perfect for content platforms, marketing sites, and blogs.",

    bestFor: [
      "Content platforms",
      "Documentation sites",
      "Marketing websites",
      "Blogs and news sites",
      "High-traffic content",
      "Static landing pages",
    ],

    teamSize: "2-10 developers",
    scalableTo: "100k+ pages",

    tradeoffs: {
      advantages: [
        "Best possible performance",
        "Unlimited scalability",
        "Low operational overhead",
        "CDN-friendly",
        "Excellent SEO",
        "Security (no server)",
        "Easy to understand",
      ],
      disadvantages: [
        "Limited interactivity",
        "Build time complexity",
        "Reduced real-time features",
        "Content updates require rebuild",
        "Limited personalization",
      ],
    },

    alternatives: ["progressive_enhancement", "lightweight_spa"],

    migration: {
      from: ["progressive_enhancement"],
      difficulty: "easy",
    },
  },

  {
    id: "fullstack_monolith",
    name: "Full-Stack Monolith (Traditional SSR)",
    description:
      "Server-rendered templates with traditional page refreshes and jQuery",

    framework: "Express/Django/Rails",
    language: "JavaScript/Python/Ruby",
    buildTool: "Webpack/none",
    styling: "Bootstrap/Tailwind",
    stateManagement: "Server session",
    testing: "Pytest/RSpec/Mocha",

    scoringFactors: {
      volume: 60, // Moderate for large projects
      latency: 50, // Page reloads have latency
      costSensitivity: 70, // Low-moderate cost
      reliability: 70, // Decent reliability
      uiComplexity: 40, // Limited for complex UIs
      timeToMarket: 70, // Familiar patterns
    },

    characteristics: {
      bundleSize: "large",
      buildTime: "fast",
      devExperience: "fair",
      scalability: "good",
      maintenance: "moderate",
      seoCapability: "excellent",
      mobileFirst: false,
      progressiveEnhancement: true,
    },

    costEstimate: {
      infrastructure: "$1k-3k/month",
      development: "3-6 weeks",
      maintenance: "$1k-2k/month",
    },

    reasoning:
      "Legacy pattern for teams familiar with server rendering. Good for gradual modernization from traditional web apps.",

    bestFor: [
      "Legacy system modernization",
      "Traditional teams",
      "Simple interactive needs",
      "Gradual migration",
      "Server-side expertise",
    ],

    teamSize: "3-10 developers",
    scalableTo: "50k LOC",

    tradeoffs: {
      advantages: [
        "Familiar patterns for traditional teams",
        "Less build complexity",
        "Easy onboarding",
        "Server-side rendering",
        "Good SEO",
        "Stateful sessions",
      ],
      disadvantages: [
        "Page refreshes on navigation",
        "Slower interactivity",
        "Larger page sizes",
        "Harder to scale interactions",
        "Mobile experience degraded",
        "Coupling frontend and backend",
      ],
    },

    alternatives: ["progressive_enhancement", "lightweight_spa"],

    migration: {
      from: [],
      difficulty: "very_hard",
    },
  },
];

/**
 * Score pattern against requirements
 * Returns confidence score 0-100
 */
export function scorePattern(
  pattern: ArchitecturePattern,
  requirements: {
    volume?: number; // 0-100
    latency?: number; // 0-100
    costSensitivity?: number; // 0-100
    reliability?: number; // 0-100
    uiComplexity?: number; // 0-100
    timeToMarket?: number; // 0-100
  }
): number {
  const factors = pattern.scoringFactors;
  const weights = {
    volume: 1.0,
    latency: 1.0,
    costSensitivity: 1.0,
    reliability: 1.0,
    uiComplexity: 1.0,
    timeToMarket: 1.0,
  };

  let score = 0;
  let totalWeight = 0;

  if (requirements.volume !== undefined) {
    score += (factors.volume * requirements.volume) / 100;
    totalWeight += weights.volume;
  }
  if (requirements.latency !== undefined) {
    score += (factors.latency * requirements.latency) / 100;
    totalWeight += weights.latency;
  }
  if (requirements.costSensitivity !== undefined) {
    score += (factors.costSensitivity * requirements.costSensitivity) / 100;
    totalWeight += weights.costSensitivity;
  }
  if (requirements.reliability !== undefined) {
    score += (factors.reliability * requirements.reliability) / 100;
    totalWeight += weights.reliability;
  }
  if (requirements.uiComplexity !== undefined) {
    score += (factors.uiComplexity * requirements.uiComplexity) / 100;
    totalWeight += weights.uiComplexity;
  }
  if (requirements.timeToMarket !== undefined) {
    score += (factors.timeToMarket * requirements.timeToMarket) / 100;
    totalWeight += weights.timeToMarket;
  }

  return totalWeight > 0 ? Math.round(score / totalWeight) : 0;
}

/**
 * Find the best matching pattern for given requirements
 */
export function findMatchingPattern(
  requirements: {
    volume?: number;
    latency?: number;
    costSensitivity?: number;
    reliability?: number;
    uiComplexity?: number;
    timeToMarket?: number;
  }
): { pattern: ArchitecturePattern; score: number; alternatives: Array<{ pattern: ArchitecturePattern; score: number }> } {
  const scores = architecturePatterns.map((pattern) => ({
    pattern,
    score: scorePattern(pattern, requirements),
  }));

  scores.sort((a, b) => b.score - a.score);

  const best = scores[0];
  const alternatives = scores.slice(1, 3); // Top 2 alternatives

  return {
    pattern: best.pattern,
    score: best.score,
    alternatives,
  };
}

/**
 * Get pattern by ID
 */
export function getPatternById(id: string): ArchitecturePattern | undefined {
  return architecturePatterns.find((p) => p.id === id);
}

/**
 * Get all patterns
 */
export function getAllPatterns(): ArchitecturePattern[] {
  return [...architecturePatterns];
}

/**
 * Compare two patterns
 */
export function comparePatterns(
  pattern1Id: string,
  pattern2Id: string
): { pattern1: ArchitecturePattern; pattern2: ArchitecturePattern; comparison: Record<string, any> } | null {
  const p1 = getPatternById(pattern1Id);
  const p2 = getPatternById(pattern2Id);

  if (!p1 || !p2) return null;

  return {
    pattern1: p1,
    pattern2: p2,
    comparison: {
      bundleSize: {
        p1: p1.characteristics.bundleSize,
        p2: p2.characteristics.bundleSize,
      },
      scalability: {
        p1: p1.characteristics.scalability,
        p2: p2.characteristics.scalability,
      },
      devExperience: {
        p1: p1.characteristics.devExperience,
        p2: p2.characteristics.devExperience,
      },
      timeToMarket: {
        p1: p1.costEstimate.development,
        p2: p2.costEstimate.development,
      },
      costEstimate: {
        p1: p1.costEstimate.infrastructure,
        p2: p2.costEstimate.infrastructure,
      },
    },
  };
}
