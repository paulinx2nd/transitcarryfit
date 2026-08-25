# Source Provenance

## Collection behavior

The contract does not browse. Rule text and source references are frozen publisher declarations; source_reference is explicitly stored as unverified.

The contract performs no live web request, does not scrape a page, and does not silently claim that a label or URL authenticates its publisher. This avoids validator drift from changing pages. If an application needs live retrieval, that retrieval belongs in a separately reviewed mechanism whose validators independently fetch and normalize the same source.

## Integrity bindings

- Contract source SHA-256: `f027a896e63e91b7b5d2f4487ccc530f0bfe505146fe3c1be4a19959144d58ff`
- ABI SHA-256: `73a60b1ff0a3389f39b458bc05df276050a871db9d7fb34bed9cd469a6d104bf`
- Frozen text and canonical JSON records are hashed inside the contract where the workflow needs a content binding.
- Human-readable source references, when present, are expressly marked unverified.

## Fixture policy

Tests use synthetic public fixtures written for this repository. They are not copied production records and do not represent real people.
