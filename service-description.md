# Engineering Verdict - service description

> 🇷🇺 [Русская версия](service-description.ru.md)

Verifying one claim about your model.

Evgeniy Dolgov. 15 years in backend and architecture. One person, not an agency.

## How it works

| YOU PROVIDE | WHAT WE DO | YOU GET |
|---|---|---|
| One claim; code and settings; data, or a run on your side | We fix criteria before the run; we reproduce the computation; we run null-data checks | Confirmed / not confirmed / not enough data; where the conclusion does not apply |

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

## Contacts and links

- Example: <https://github.com/sensus-stoa/permutation-test-ml> - synthetic data; not yet tested on real power-sector data
- Verification protocol: [https://github.com/sensus-stoa/permutation-test-ml/tree/main/trust](https://github.com/sensus-stoa/permutation-test-ml/tree/main/trust)
- Detailed description: [FILL IN: link to the detailed description]
- Contact: beattle1984@gmail.com · LinkedIn [FILL IN: profile URL]

---

The canonical text of the service is `one-pager.typ` (its copy lives in `README.md`,
this file is a synced version of the same text). Text and number edits are the
owner's call; the document builds with `typst compile one-pager.typ one-pager.pdf`.
