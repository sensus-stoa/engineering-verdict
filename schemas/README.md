# Schemas

Machine-readable contracts for the Engineering Verdict service. Three schemas, three fillable forms, one validator. All JSON Schema draft-07.

## Schemas

| File | What it gates | Required core |
|---|---|---|
| `intake.schema.json` | the client brief | `claim` (non-blank, `\S`), `code_and_settings`, `data_or_run` |
| `evidence-manifest.schema.json` | the evidence bundle | `object{repo, commit}`, `criteria_lock{commit, date, note}`, `evidence[]` (id, type, path or url, sha256, role, disclosure), `controls[]` (id, N) |
| `verdict.schema.json` | the verdict | `verdict_id`, `date`, `valid_until`, `object_version`, `executor`, `verifier`, `claims[]`, `properties_separate{integrity, provenance, reproducibility, validity}` |

Frozen by design: statuses are exactly `PASS | FAIL | INCONCLUSIVE`; the `reason_code` enum is exactly DATA, GRAMMAR, NOISE, DEPTH, ACCESS, BUDGET, ENVIRONMENT, CONFLICT_EVIDENCE, OUT_OF_SCOPE; `protocol_version` is `CV0-TrustLayer-v3.5` (v3.6 is the map version, not the protocol).

## Conditional rules (if/then, not prose)

- `status` FAIL or INCONCLUSIVE -> `reason_code` required.
- `status` PASS or FAIL -> `verification` + `evidence[]` required.
- claim `kind=reliability` with `status=PASS` -> `control` required.
- evidence `sha256: null` -> explanatory `note` required.
- disclosure: `public | client | sealed` only.
- roles: two vocabularies, no mixing within one manifest (incident I-002 in the example repository): the spec §3.7 set (`client-generated`, `client-executed`, `provider-verified`, `independently reproduced`) for client engagements; the `author-*` set only for public self-audit without a client.

## Forms

`templates/*.example.json` are fillable forms; keys prefixed with `_` are guidance and allowed by the schemas. `intake.example.json` validates even before filling (the hard gate is the non-blank claim); the evidence and verdict forms validate after filling, when the hash formats are in place.

## Validator

`intake_validate.py` (python3, jsonschema):

- no arguments: built-in battery, 17 cases across all three schemas, including negative controls NEG-1..NEG-6 (a schema that accepts everything is useless);
- `python3 schemas/intake_validate.py MANIFEST.json VERDICT.json`: live mode - validates real files and runs the referential checks draft-07 cannot express (referenced controls exist with an N, claim evidence ids resolve in the manifest, sha-null items carry a note).

Exit code 0 = every case matched. Run it before any commit that touches trust artifacts.

## Provenance

The evidence and verdict schemas were derived from the published worked example V-PTM-001 (`permutation-test-ml/trust/`), not invented: the live manifest and verdict pass both schemas as-is.
