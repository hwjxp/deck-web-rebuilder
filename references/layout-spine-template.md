# Layout Spine Template

Copy this into `40-rebuild/layout-spine.md` before writing page specs.

Format:

```text
slide-NN | PATTERN-NAME | slide-role | one-line visual intent
```

Example:

```text
slide-01 | HERO-FULL      | cover         | dark hero field with one-line opening claim
slide-02 | HEADLINE-PROOF | framing       | claim on top, one proof object below
slide-03 | DIAGRAM-CENTER | proof         | centered venn or matrix with attached notes
slide-04 | SPLIT-60-40    | showcase      | primary sample left, interpretation rail right
slide-05 | TIMELINE-H     | process       | left-to-right staged rollout with short node labels
```

## Rhythm Validation Checklist

Run these checks before locking the spine:

- Are there three or more consecutive `HERO-FULL` slides?
- Are there four or more consecutive grid slides?
- Are two adjacent `HEADLINE-PROOF` slides repeating the same exact proof posture?
- Does the deck have at least some breathing-point slides if it runs longer than 10-15 slides?

If any answer is yes, revise the spine before moving into `layout-plan.json` or `page-specs.*`.
