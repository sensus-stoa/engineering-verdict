#!/usr/bin/env python3
# Validate schemas/intake.schema.json with a real validator - 5 cases.
# Run: python3 schemas/intake_validate.py  (exit code 0 = every case matched)
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft7Validator
except ImportError:
    sys.exit("jsonschema library missing: pip install jsonschema")

schema = json.loads(
    (Path(__file__).resolve().parent / "intake.schema.json").read_text(encoding="utf-8")
)
validator = Draft7Validator(schema)

base = {
    "claim": "an example claim about the model",
    "code_and_settings": "link to the saved code version and settings",
    "data_or_run": "a depersonalized fragment or a run on the client's side",
}

cases = [
    ("valid: all three fields filled", dict(base), True),
    ("valid: three fields + one extra", {**base, "notes": "an extra field"}, True),
    ("invalid: claim missing", {k: v for k, v in base.items() if k != "claim"}, False),
    ("invalid: claim = empty string", {**base, "claim": ""}, False),
    ("invalid: claim = whitespace only", {**base, "claim": "   "}, False),
]

failures = 0
for name, payload, expected in cases:
    errors = sorted(validator.iter_errors(payload), key=lambda e: e.json_path)
    ok = not errors
    verdict = "OK" if ok == expected else "MISMATCH"
    if ok != expected:
        failures += 1
    print(f"[{verdict}] {name} -> {'valid' if ok else 'invalid'}")
    for e in errors:
        print(f"       {e.json_path}: {e.message}")

sys.exit(1 if failures else 0)
