# Verifying one claim about your model

> 🇷🇺 [Русская версия](README.ru.md)

Evgeniy Dolgov. 15 years in backend and architecture. One person, not an agency.

**YOU PROVIDE:** One claim. Code and settings. Data, or a run on your side.

**WHAT WE DO:** We fix criteria before the run. We reproduce the computation. We run null-data checks.

**YOU GET:** Confirmed / not confirmed / not enough data. Where the conclusion does not apply.

## A typical failure

The model showed 3% error in tests and 12% in production. The tests fed it the actual
weather for the same day. In production only the forecast is available in advance.
The model was looking into the future, and the test did not catch it.

## Why you can trust this

In our open example, a naive check took pure noise for signal in 36 of 50 cases.
We measured it and published it, along with the cases where our method does not work.
How many errors our own procedure misses will be published before the first paid check.

## Price and timeline

Reference: 800-1200 EUR, exact price after a scope assessment, 3-5 business days
from receiving the materials.

## What we do not do

We do not train the model. We do not issue a certificate. We do not promise it will never break.

## Contacts

- Example: [github.com/sensus-stoa/permutation-test-ml](https://github.com/sensus-stoa/permutation-test-ml) - synthetic data; not yet tested on real power-sector data
- Verification protocol: [https://github.com/sensus-stoa/permutation-test-ml/tree/main/trust](https://github.com/sensus-stoa/permutation-test-ml/tree/main/trust)
- Detailed description: [FILL IN: link to the detailed description]
- Contact: beattle1984@gmail.com · LinkedIn [FILL IN: profile URL]

---

Build the PDF: `typst compile one-pager.typ one-pager.pdf` (Typst 0.15+).
Russian surface: `one-pager-ru.typ` builds `one-pager-ru.pdf` (its text lives in README.ru.md).
The one-pager text is agreed; text and number edits are the owner's call.
