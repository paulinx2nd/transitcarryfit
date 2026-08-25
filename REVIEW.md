# Reviewer Guide

## Mechanism in one sentence

A reusable multi-leg carry workflow where each frozen carrier-rule snapshot is assessed independently and code seals the itinerary with the strictest leg status.

## What consensus actually decides

Validators agree separately on ALLOWED, RESTRICTED, PROHIBITED, or UNKNOWN for each leg.

## What code settles afterward

Every leg stores its own result and a deterministic severity ranking produces the final strictest status only after all legs finish.

## Why this is distinct

The mechanism is repeated per-leg consensus followed by a strictest-route reducer.

## Fast review path

1. Confirm the pinned dependency on the first source line.
2. Inspect the custom validator and verify it reruns the substantive task.
3. Trace role checks and terminal-state guards in each write method.
4. Run lint, strict type checking, seven direct tests, and the five-validator integration test.
5. Compare `abi.json` and the StudioNet manifest to the committed source hash.

## Known limitations

Rules can be stale or misquoted and publishers are not authenticated carriers. This is not security, customs, or legal clearance.
