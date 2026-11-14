#!/usr/bin/env python3
# Validate engineering-verdict schemas with a real validator (jsonschema, draft-07).
#
# Coverage:
#   intake            - 5 cases (client product brief)
#   evidence-manifest - 3 cases (valid / bad disclosure / sha256-null without note)
#   verdict           - 4 cases: valid + NEGATIVE CONTROLS:
#       NEG-1: reliability claim (kind=reliability) with PASS and no control  -> must reject
#       NEG-2: INCONCLUSIVE claim without reason_code                         -> must reject
#       NEG-3: verdict without valid_until                                    -> must reject
#       NEG-4 (live mode): the published V-PTM-001 must be ACCEPTED
#
# Usage:
#   python3 schemas/intake_validate.py
#       built-in battery for all three schemas; exit 0 = every case matched.
#   python3 schemas/intake_validate.py MANIFEST.json VERDICT.json
#       live mode: validate real files against the schemas + referential checks
#       (claim.control references an existing control with N; claim.evidence ids
#       exist in the manifest; sha256:null items carry an explanatory note).
import json
import sys
from copy import deepcopy
from pathlib import Path

try:
    from jsonschema import Draft7Validator
except ImportError:
    sys.exit("jsonschema library missing: pip install jsonschema")

SCHEMA_DIR = Path(__file__).resolve().parent


def load_schema(name):
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def run_cases(schema_name, validator, cases):
    failures = 0
    for label, payload, expected in cases:
        errors = sorted(validator.iter_errors(payload), key=lambda e: list(e.absolute_path))
        ok = not errors
        verdict = "OK" if ok == expected else "MISMATCH"
        if ok != expected:
            failures += 1
        print(f"[{verdict}] {schema_name}: {label} -> {'valid' if ok else 'invalid'}")
        for e in errors:
            path = "/".join(str(p) for p in e.absolute_path) or "$"
            print(f"       {path}: {e.message}")
    return failures


def referential_checks(manifest, verdict):
    """Cross-file rules draft-07 cannot express: control refs exist with N, evidence ids resolve."""
    findings = []
    controls = {}
    for c in manifest.get("controls", []):
        controls[c["id"]] = c
    for c in verdict.get("negative_controls", []):
        controls.setdefault(c["id"], c)
    evidence_ids = {e["id"] for e in manifest.get("evidence", [])}

    for claim in verdict.get("claims", []):
        cid = claim.get("id", "?")
        if "control" in claim:
            ref = claim["control"]
            if ref not in controls:
                findings.append(f"claim {cid}: control '{ref}' not found in manifest.controls / verdict.negative_controls")
            elif not isinstance(controls[ref].get("N"), int) or controls[ref]["N"] < 1:
                findings.append(f"claim {cid}: control '{ref}' has no usable N")
        for ev in claim.get("evidence", []):
            if ev not in evidence_ids:
                findings.append(f"claim {cid}: evidence id '{ev}' not found in manifest.evidence")
    for e in manifest.get("evidence", []):
        if e.get("sha256", "x") is None and not e.get("note"):
            findings.append(f"evidence {e.get('id', '?')}: sha256 is null without explanatory note")
    return findings


def built_in_battery():
    failures = 0
    A40, B40, C64 = "a" * 40, "b" * 40, "c" * 64

    intake_v = Draft7Validator(load_schema("intake.schema.json"))
    base = {
        "claim": "an example claim about the model",
        "code_and_settings": "link to the saved code version and settings",
        "data_or_run": "a depersonalized fragment or a run on the client's side",
    }
    intake_cases = [
        ("valid: all three fields filled", dict(base), True),
        ("valid: three fields + one extra", {**base, "notes": "an extra field"}, True),
        ("invalid: claim missing", {k: v for k, v in base.items() if k != "claim"}, False),
        ("invalid: claim = empty string", {**base, "claim": ""}, False),
        ("invalid: claim = whitespace only", {**base, "claim": "   "}, False),
    ]
    failures += run_cases("intake", intake_v, intake_cases)

    manifest_v = Draft7Validator(load_schema("evidence-manifest.schema.json"))
    manifest_ok = {
        "schema": "trust-manifest/v3.5",
        "protocol_version": "CV0-TrustLayer-v3.5",
        "date": "2026-11-13",
        "object": {"repo": "https://github.com/owner/repo", "commit": A40},
        "criteria_lock": {"commit": B40, "date": "2026-11-12", "note": "criteria fixed before the run"},
        "evidence": [
            {"id": "E-01", "type": "code", "path": "src/main.py", "sha256": C64,
             "role": "client-generated", "disclosure": "public"},
            {"id": "E-02", "type": "run-output", "path": "results/out.csv", "sha256": None,
             "role": "client-executed", "disclosure": "client",
             "note": "results/ is gitignored; regenerate with: python run.py"},
        ],
        "controls": [
            {"id": "NC-X", "description": "pure noise, H0 true", "N": 40,
             "rejections": 2, "rate": 0.05, "wilson_ci_95": [0.01, 0.15]},
        ],
    }
    m_bad_disclosure = deepcopy(manifest_ok)
    m_bad_disclosure["evidence"][0]["disclosure"] = "internal"
    m_bad_sha = deepcopy(manifest_ok)
    del m_bad_sha["evidence"][1]["note"]
    manifest_cases = [
        ("valid: minimal manifest (path+sha, url-type allowed, null+note sha)", manifest_ok, True),
        ("invalid: disclosure outside public|client|sealed", m_bad_disclosure, False),
        ("invalid: sha256 null without explanatory note", m_bad_sha, False),
    ]
    failures += run_cases("evidence-manifest", manifest_v, manifest_cases)

    verdict_v = Draft7Validator(load_schema("verdict.schema.json"))
    verdict_ok = {
        "schema": "trust-verdict/v3.5",
        "verdict_id": "V-EXAMPLE-001",
        "date": "2026-11-13",
        "valid_until": "object-change",
        "object_version": A40,
        "protocol_version": "CV0-TrustLayer-v3.5",
        "executor": "Client (author)",
        "verifier": "Provider; independent verification pending",
        "claims": [
            {"id": "C-01", "status": "PASS", "kind": "reliability",
             "verification": "V-01: repeated runs N=40", "evidence": ["E-01", "E-02"],
             "control": "NC-X", "note": "CI contains 0.05"},
            {"id": "C-02", "status": "INCONCLUSIVE", "reason_code": "ACCESS",
             "note": "sealed data not provided"},
        ],
        "properties_separate": {
            "integrity": "sha256 per evidence item",
            "provenance": "client-generated + provider-verified",
            "reproducibility": "author-executed; independent: pending",
            "validity": "C-02 marks the applicability boundary",
        },
        "negative_controls": [
            {"id": "NC-X", "N": 40, "false_rejections": 2, "rate": 0.05, "wilson_ci_95": [0.01, 0.15]},
        ],
    }
    v_neg1 = deepcopy(verdict_ok)
    del v_neg1["claims"][0]["control"]
    v_neg2 = deepcopy(verdict_ok)
    del v_neg2["claims"][1]["reason_code"]
    v_neg3 = deepcopy(verdict_ok)
    del v_neg3["valid_until"]
    verdict_cases = [
        ("valid: minimal verdict (reliability PASS with control; INCONCLUSIVE with reason_code)", verdict_ok, True),
        ("NEG-1: reliability PASS without control -> must reject", v_neg1, False),
        ("NEG-2: INCONCLUSIVE without reason_code -> must reject", v_neg2, False),
        ("NEG-3: verdict without valid_until -> must reject", v_neg3, False),
    ]
    failures += run_cases("verdict", verdict_v, verdict_cases)

    refs = referential_checks(manifest_ok, verdict_ok)
    print(f"[{'OK' if not refs else 'MISMATCH'}] referential: control refs + evidence ids + sha-notes")
    for f in refs:
        print(f"       {f}")
    return failures + (1 if refs else 0)


def live_mode(manifest_path, verdict_path):
    failures = 0
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    verdict = json.loads(Path(verdict_path).read_text(encoding="utf-8"))
    print(f"live: {manifest_path}")
    failures += run_cases(
        "evidence-manifest (live)",
        Draft7Validator(load_schema("evidence-manifest.schema.json")),
        [("published V-PTM-001 manifest must be accepted", manifest, True)],
    )
    print(f"live: {verdict_path}")
    failures += run_cases(
        "verdict (live)",
        Draft7Validator(load_schema("verdict.schema.json")),
        [("published V-PTM-001 verdict must be accepted", verdict, True)],
    )
    refs = referential_checks(manifest, verdict)
    print(f"[{'OK' if not refs else 'MISMATCH'}] live referential checks")
    for f in refs:
        print(f"       {f}")
    return failures + (1 if refs else 0)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 2:
        exit_code = live_mode(args[0], args[1])
    elif len(args) == 0:
        exit_code = built_in_battery()
    else:
        print("usage: intake_validate.py [MANIFEST.json VERDICT.json]", file=sys.stderr)
        exit_code = 2
    sys.exit(1 if exit_code else 0)
