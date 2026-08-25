# Originality

## Mechanism fingerprint

The mechanism is repeated per-leg consensus followed by a strictest-route reducer.

Lifecycle: publish rule snapshots -> open ordered trip -> assess each leg -> deterministic strictest aggregation -> seal or cancel.

Consensus boundary: Validators agree separately on ALLOWED, RESTRICTED, PROHIBITED, or UNKNOWN for each leg.

Settlement boundary: Every leg stores its own result and a deterministic severity ranking produces the final strictest status only after all legs finish.

## Review-cohort defense

Names, prompts, labels, and method names are not the basis of the distinction. The actor topology, stored state, allowed transitions, validator decision, and deterministic settlement described above are the reusable mechanism. A full-workspace structural scan is run before publication; its JSON report is retained outside the repository-wide source tree and summarized in `AUDIT.md` after the final pass.
