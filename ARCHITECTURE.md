# Architecture

## Boundary

- Frontend or backend: wallet UX, indexing, private drafts, non-authoritative previews, notifications, and optional off-chain source retrieval.
- GenLayer contract: Validators agree separately on ALLOWED, RESTRICTED, PROHIBITED, or UNKNOWN for each leg. Every leg stores its own result and a deterministic severity ranking produces the final strictest status only after all legs finish.
- External world: The contract does not browse. Rule text and source references are frozen publisher declarations; source_reference is explicitly stored as unverified.

## Event path

publish rule snapshots -> open ordered trip -> assess each leg -> deterministic strictest aggregation -> seal or cancel

## Actors

- rule publishers
- traveler
- GenLayer validators

## Consensus design

The leader produces a normalized bounded result. Each validator independently reruns the substantive task from the same frozen public inputs. Validators compare the decision fields that change state, not merely JSON shape. Invalid model output raises `[LLM_ERROR]` so a broken leader is not accepted.

## Deterministic layer

Every leg stores its own result and a deterministic severity ranking produces the final strictest status only after all legs finish. Identifiers, bounds, access checks, ordering, counters, masks, hashes, and terminal-state guards are computed deterministically.

## Persistence

State uses GenLayer storage types only. Public composite records are serialized as canonical JSON where appropriate. Source SHA-256 at evidence generation: `f027a896e63e91b7b5d2f4487ccc530f0bfe505146fe3c1be4a19959144d58ff`.
