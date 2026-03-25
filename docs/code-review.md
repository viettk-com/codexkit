# Code review rubric

Review with this order of importance:

1. correctness and regression risk
2. security and trust boundaries
3. missing or weak validation
4. maintainability and architecture drift
5. performance, operability, and rollback gaps

## Ask these questions

- Does the diff truly solve the intended problem?
- Did the code stay inside the right boundary?
- Are edge cases and failure modes handled?
- Is any public behavior or contract changed silently?
- What evidence shows the change is safe?
- Did docs, runbooks, or release notes need updates?

## Severity model

- **Blocker**: must fix before merge or ship
- **High**: likely real bug or serious risk
- **Medium**: quality or maintainability issue worth fixing soon
- **Low**: optional polish
