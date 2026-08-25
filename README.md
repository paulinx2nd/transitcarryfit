# TransitCarryFit

A reusable multi-leg carry workflow where each frozen carrier-rule snapshot is assessed independently and code seals the itinerary with the strictest leg status.

## Why GenLayer

Validators agree separately on ALLOWED, RESTRICTED, PROHIBITED, or UNKNOWN for each leg. Every leg stores its own result and a deterministic severity ranking produces the final strictest status only after all legs finish.

## Roles

- rule publishers
- traveler
- GenLayer validators

## Lifecycle

publish rule snapshots -> open ordered trip -> assess each leg -> deterministic strictest aggregation -> seal or cancel

## Contract interface

- Constructor: none
- Write methods: assess_leg, cancel_trip, open_trip, publish_rule, retire_rule, seal_trip
- View methods: get_rule, get_rule_count, get_rule_id, get_trip, get_trip_count, get_trip_id
- Runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

## Public-data warning

All contract inputs, evidence, notes, addresses, model results, and state are public. Do not submit secrets, private documents, personal contact information, or confidential identifiers.

## Source model

The contract does not browse. Rule text and source references are frozen publisher declarations; source_reference is explicitly stored as unverified.

## Verification

```text
genvm-lint check contracts/transit_carry_fit.py
genvm-lint typecheck contracts/transit_carry_fit.py --strict
python -m pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
python -m pytest tests/integration -q -s
```

The repository contains seven direct tests and one full five-validator GLSim flow. StudioNet evidence is recorded separately under `deployments/` after network execution.

## Limitations

Rules can be stale or misquoted and publishers are not authenticated carriers. This is not security, customs, or legal clearance.

Licensed under MIT. See `LICENSE`.
