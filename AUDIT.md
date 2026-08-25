# Audit Record

Audit date: 2026-08-25

## Automated results

- GenVM lint and SDK validation: PASS
- Strict Pyright through genvm-lint: PASS
- Direct-mode tests: 7 PASS
- Five-validator GLSim integration: 1 PASS
- ABI regenerated from final source: PASS
- Pinned runner header: PASS
- Dependency vulnerability audit: PASS, zero known vulnerabilities
- Full-workspace structural originality scan: PASS, 121 contracts scanned; every nearest external match is below 0.35 and has a different public method shape
- StudioNet: PASS - fresh owner-isolated wallets, all transactions finalized and executed successfully, deployed source/schema matched, and mechanism-specific bound state read back
- GitHub publication: PASS - private remote and clean one-commit reachable history verified

## Artifact hashes

- Source: `f027a896e63e91b7b5d2f4487ccc530f0bfe505146fe3c1be4a19959144d58ff`
- ABI: `73a60b1ff0a3389f39b458bc05df276050a871db9d7fb34bed9cd469a6d104bf`

## Manual findings

The substantive validator independently reruns the task. The contract documents caller-attested source limitations, public-data exposure, role boundaries, terminal states, and residual risk. The mechanism is repeated per-leg consensus followed by a strictest-route reducer. The StudioNet manifest records the contract address, transaction receipts, fresh public test roles, exact source and schema readback, and the mechanism-specific terminal assertion.
