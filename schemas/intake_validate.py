#!/usr/bin/env python3
# Проверка schemas/intake.schema.json реальным валидатором — 4 случая.
# Запуск: python3 schemas/intake_validate.py  (код возврата 0 = все случаи сошлись)
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft7Validator
except ImportError:
    sys.exit("нет библиотеки jsonschema: pip install jsonschema")

schema = json.loads(
    (Path(__file__).resolve().parent / "intake.schema.json").read_text(encoding="utf-8")
)
validator = Draft7Validator(schema)

base = {
    "claim": "пример утверждения о модели",
    "code_and_settings": "ссылка на сохранённую версию кода и настройки",
    "data_or_run": "обезличенный фрагмент либо запуск на стороне клиента",
}

cases = [
    ("valid: все три поля заполнены", dict(base), True),
    ("valid: три поля + одно дополнительное", {**base, "notes": "дополнительное поле"}, True),
    ("invalid: отсутствует claim", {k: v for k, v in base.items() if k != "claim"}, False),
    ("invalid: claim = пустая строка", {**base, "claim": ""}, False),
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
