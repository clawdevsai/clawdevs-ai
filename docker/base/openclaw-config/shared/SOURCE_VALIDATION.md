# Source Validation Contract

## Purpose

Define the validation protocol for external information before using it for critical decisions. Prevents misinformation, outdated data, and unreliable sources from influencing agent behavior.

Referenced in CONSTITUTION.md: "Source Validation Contract: For external-information decisions, enforce SOURCE_VALIDATION.md in the active workspace (3 independent sources, 1 official source, explicit dates, confidence)."

---

## Core Principle

**Never trust a single source.** All external information must pass multi-source validation before informing critical decisions.

```
External Information → Validate Source → Check Temporal →
Cross-validate → Grade Evidence → Decision Safe ✓
```

---

## Source Categories & Trust Levels

### Tier 1: Official Sources (Trust = 0.95-1.0)

- Official documentation (docs.python.org, github.com official)
- Published standards (RFC 3986, ISO 8601)
- Official changelog/release notes
- Vendor official blog

**Validation**: Verify domain ownership, check dates, confirm identity
**Minimum sources**: 1 official source sufficient IF recent

### Tier 2: Peer-Reviewed (Trust = 0.80-0.95)

- Stack Overflow (1000+ upvotes)
- Academic papers (arxiv, journals)
- Technical books (O'Reilly)
- Trusted open-source projects (1000+ stars)

**Validation**: Check author credentials, verify venue quality
**Minimum sources**: Need 2-3 sources

### Tier 3: Community (Trust = 0.60-0.80)

- Hacker News discussions with experts
- Reddit communities with consensus
- Expert blog posts
- GitHub issues/discussions

**Validation**: Multiple corroborating sources, look for dissent
**Minimum sources**: Need 3+ sources

### Tier 4: Secondary (Trust = 0.40-0.70)

- Medium articles, dev.to posts
- YouTube tutorials
- Tech blogs
- Tutorials and how-to guides

**Validation**: Cross-check against primary sources
**Minimum sources**: Need 2+ independent sources, never as sole evidence

### Tier 5: Unverified (Trust = 0.0-0.40)

- Random tweets, Discord messages
- Unmoderated forums
- Anonymous sources
- Single-source blog posts

**Validation**: Requires extraordinary evidence, 5+ sources (Tier 2+)
**NEVER use for critical decisions without verification**

---

## The Three-Source Rule

**For ANY external-information decision:**

```
IF 3+ diverse sources with consensus:
    USE confidence score
ELIF 2+ sources with 1 official and recent:
    USE confidence * 0.9
ELIF 1 official source and recent:
    USE confidence * 0.8
ELIF single non-official:
    REJECT (confidence = 0)
```

---

## Temporal Validation

### Age Thresholds

| Category | Max Age | Needs Verification |
|----------|---------|-------------------|
| Language docs | 30 days | After 30 days |
| Library docs | 7 days | After 7 days |
| API docs | 1 day | After 1 day |
| Security advisories | 1 hour | After 1 hour |
| Performance benchmarks | 7 days | After 7 days |
| Best practices | 90 days | After 90 days |

### Every Source Must Have

- ✅ Publication date (when published?)
- ✅ Last updated date (when verified?)
- ✅ Validity range (if applicable)
- ✅ Temporal context (e.g., "as of Python 3.11")

**Without explicit dates → Zero trust (unless official)**

---

## Confidence Scoring (0-1.0)

```yaml
Calculation:
  base: 0.0
  + tier1_official: 0.40
  + tier2_peerreviewed: 0.30
  + tier3_community: 0.20
  + per_additional_source: 0.15 (max +0.30)
  + fresh_bonus: 0.10 (< 7 days)
  - stale_penalty: 0.20 (> 90 days)
  - archival_penalty: 0.50 (> 1 year)
  + full_consensus: 0.15
  - major_conflict: 0.30

Decision Thresholds:
  >= 0.85: HIGH confidence (safe to use)
  0.70-0.85: MEDIUM (use with caution)
  0.50-0.70: LOW (escalate to human)
  < 0.50: REJECT (don't use)
```

---

## Contradiction Resolution

**When sources disagree:**

1. Identify points of disagreement
2. Grade each source (Tier + Temporal)
3. Weight highest-tier recent sources
4. If unresolved → ESCALATE TO HUMAN
5. Log contradiction for audit trail

**Priority for conflicts:**
1. Official recent > All others
2. Multiple Tier 2 recent > Single Tier 1 old
3. Unresolved conflict > Lowest-confidence decision

---

## Best Practices

### ✅ DO

1. Require 3 sources for important decisions
2. Prefer official sources even if older
3. Check dates explicitly
4. Cross-check claims against officials
5. Log contradictions
6. Escalate low-confidence decisions
7. Document reasoning
8. Update old sources with recent findings
9. Trust peer-review but verify with officials
10. Question single sources regardless of author

### ❌ DON'T

1. Never use Tier 5 for critical decisions
2. Don't trust age alone; verify dates explicitly
3. Don't assume author expertise without verification
4. Don't ignore contradictions
5. Don't use old sources without checking updates
6. Don't skip validation because "it seems obvious"
7. Don't trust secondary sources without checking primary
8. Don't accept single sources (except Tier 1 official)
9. Don't use anonymous/unnamed sources
10. Don't proceed if confidence < 0.70 without human approval

---

## Integration with Agent Loop

### Before Using External Information

1. Is information external-sourced?
   - YES → Continue
   - NO → Use normally

2. Gather sources (official, peer-reviewed, community)

3. Grade each source (Tier + Temporal + Author)

4. Compute confidence score

5. Decision:
   - >= 0.85 → Use it
   - 0.70-0.85 → Use with caution, log
   - 0.50-0.70 → Escalate to human
   - < 0.50 → REJECT

---

## Monitoring

### Track

- Total external-info decisions
- Pass/fail validation rate
- Escalations to human
- Confidence distribution
- Source tier usage
- Contradictions found

### Commands

```bash
openclaw validation history --days 7
openclaw validation rejections --period 24h
openclaw validation escalations --agent dev_backend
openclaw validation sources --breakdown
```

---

**Remember**: Trust, but verify. Verify, but test. Test, but audit.
