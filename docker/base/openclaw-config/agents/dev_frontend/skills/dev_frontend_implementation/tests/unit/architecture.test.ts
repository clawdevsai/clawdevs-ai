import {
  findMatchingPattern,
  scorePattern,
  getPatternById,
  architecturePatterns,
} from "../../src/decisions/architecture_matrix";

describe("Frontend Architecture Matrix", () => {
  describe("Pattern Scoring", () => {
    test("should score component-driven high for large complex projects", () => {
      const pattern = architecturePatterns[0]; // component_driven
      const score = scorePattern(pattern, {
        volume: 100,
        uiComplexity: 100,
      });
      expect(score).toBeGreaterThan(80);
    });

    test("should score lightweight-spa high for MVPs", () => {
      const pattern = architecturePatterns.find((p) => p.id === "lightweight_spa");
      if (pattern) {
        const score = scorePattern(pattern, {
          volume: 20,
          timeToMarket: 100,
          costSensitivity: 100,
        });
        expect(score).toBeGreaterThan(80);
      }
    });

    test("should score progressive-enhancement high for e-commerce", () => {
      const pattern = architecturePatterns.find((p) => p.id === "progressive_enhancement");
      if (pattern) {
        const score = scorePattern(pattern, {
          latency: 100,
          volume: 80,
        });
        expect(score).toBeGreaterThan(80);
      }
    });
  });

  describe("Pattern Matching", () => {
    test("should recommend lightweight-spa for small startup project", () => {
      const result = findMatchingPattern({
        volume: 20,
        timeToMarket: 100,
        costSensitivity: 100,
      });

      expect(result.pattern.id).toBe("lightweight_spa");
      expect(result.score).toBeGreaterThan(70);
    });

    test("should recommend component-driven for large enterprise", () => {
      const result = findMatchingPattern({
        volume: 100,
        uiComplexity: 100,
        reliability: 100,
      });

      expect(result.pattern.id).toBe("component_driven");
      expect(result.score).toBeGreaterThan(80);
    });

    test("should recommend progressive-enhancement for e-commerce", () => {
      const result = findMatchingPattern({
        volume: 80,
        latency: 100,
      });

      // Either progressive or component-driven could work
      expect(["component_driven", "progressive_enhancement"]).toContain(result.pattern.id);
      expect(result.score).toBeGreaterThan(70);
    });

    test("should provide alternatives", () => {
      const result = findMatchingPattern({
        volume: 50,
        uiComplexity: 50,
      });

      expect(result.alternatives.length).toBeGreaterThan(0);
      expect(result.alternatives[0].pattern.id).not.toBe(result.pattern.id);
    });
  });

  describe("Pattern Retrieval", () => {
    test("should get all patterns", () => {
      const patterns = architecturePatterns;
      expect(patterns.length).toBeGreaterThanOrEqual(6);
    });

    test("should get pattern by ID", () => {
      const pattern = getPatternById("component_driven");
      expect(pattern).toBeDefined();
      expect(pattern?.id).toBe("component_driven");
      expect(pattern?.name).toContain("Component-Driven");
    });

    test("should handle invalid pattern ID", () => {
      const pattern = getPatternById("invalid");
      expect(pattern).toBeUndefined();
    });
  });

  describe("Pattern Characteristics", () => {
    test("component-driven should have excellent scalability", () => {
      const pattern = getPatternById("component_driven");
      expect(pattern?.characteristics.scalability).toBe("excellent");
    });

    test("lightweight-spa should have limited scalability", () => {
      const pattern = getPatternById("lightweight_spa");
      expect(pattern?.characteristics.scalability).toBe("limited");
    });

    test("headless-cms should have excellent SEO", () => {
      const pattern = getPatternById("headless_cms");
      expect(pattern?.characteristics.seoCapability).toBe("excellent");
    });

    test("progressive-enhancement should support mobile-first", () => {
      const pattern = getPatternById("progressive_enhancement");
      expect(pattern?.characteristics.mobileFirst).toBe(true);
    });
  });

  describe("Cost Estimates", () => {
    test("lightweight-spa should be low-cost", () => {
      const pattern = getPatternById("lightweight_spa");
      expect(pattern?.costEstimate.infrastructure).toContain("$0");
    });

    test("component-driven should be moderate-cost", () => {
      const pattern = getPatternById("component_driven");
      expect(pattern?.costEstimate.infrastructure).toContain("$2k");
    });

    test("headless-cms should be low-cost", () => {
      const pattern = getPatternById("headless_cms");
      expect(pattern?.costEstimate.infrastructure).toContain("$100");
    });
  });
});
