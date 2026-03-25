# Systematic debugging

When the root cause is unknown, treat debugging like investigation work.

## Workflow

1. Capture symptom and expected behavior
2. Build the best minimal repro
3. Write a short ordered hypothesis list
4. Eliminate causes with targeted evidence
5. Isolate root cause before broad edits
6. Add a durable regression guard
7. Record the lesson in continuity memory if it is reusable

## Evidence over intuition

Prefer:
- failing tests
- logs with timestamps and request identifiers
- browser console or network traces
- metrics or alerts around the failing path
- narrow probes against a specific layer or module

Avoid:
- speculative multi-file fixes
- changing code before a plausible repro exists
- merging a fix without a guard against recurrence
