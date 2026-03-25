# Architecture review checklist

Use this when validating `architecture.md`, `decision-matrix.md`, or an ADR.

## Problem framing
- Is the real problem clear?
- Are non-goals explicit?
- Is the change class correct?

## Boundary quality
- Does the capability live in the right module or service?
- Is ownership explicit?
- Are dependencies pointing the right way?

## Contract quality
- Are APIs, events, or schemas clear?
- Is backward compatibility handled?
- Are versioning and migration needs explicit?

## Data and state
- Where does state live?
- What invariants must hold?
- Is consistency strategy clear?

## Operability
- Are logs, metrics, traces, alerts, and dashboards defined?
- Is there a believable rollback or degradation mode?
- Is the on-call burden acceptable?

## Scale and cost
- Are latency, throughput, and volume assumptions explicit?
- Are hot paths and likely bottlenecks identified?
- Is the chosen architecture proportionate to expected growth?

## Delivery
- Can the change be implemented in safe slices?
- Are validation commands defined?
- Is there an ADR for durable design choices?
