# Independent verification of a forecast or degradation model

> 🇷🇺 [Русская версия](service-description.ru.md)

Draft, revision 13.11.2026. Terms valid until February 4, 2027
or until the object of verification changes.

## 1. In short

We check whether the stated accuracy of your model can be trusted.
We do not train it and we do not improve it. We take one specific claim -
for example, "the forecast error one day ahead does not exceed 5%" - and see
whether it survives an honest check: on data the model has not seen, and under
conditions that match real operation.

The result is a written report with one of three outcomes: the claim is
confirmed, not confirmed, or there is not enough data. In the last case
we write exactly what is missing.

## 2. Why this matters: an example

A company forecasts electricity consumption one day ahead in order to buy
the right volume in advance. In tests the model shows a 3% error.
In real operation, 12%.

The cause turned out to be in the design of the check: in tests the model was
fed the actual weather for the same day. In real operation only the weather
forecast is available the day before. The model was involuntarily looking
into the future, and the test did not catch it.

The model itself was fine. The check was the defect. Such defects are not
visible in accuracy reports - they show up only if you take apart how exactly
the test is built.

## 3. Who this is for

- Forecast developers (load, generation, prices): they have a model
  and a stated accuracy that must be confirmed to a customer.
- Developers of battery wear and remaining life models: they need to show
  that the accuracy holds outside the training sample.
- Integrators and consulting teams: they need a second opinion
  on a contractor's result.
- Those preparing technical justification for a third party:
  a customer, an investor, an internal auditor.

## 4. What we do

1. Before the work starts, we record in writing what counts as success and
   what counts as failure. The record is kept with a date from before we see
   any results. This protects against tuning the criteria to a preferred
   answer. The lock is mechanical: the criteria text is committed before the
   run, and the lock commit hash is a required field of the evidence bundle.
2. We reproduce your computation in a clean environment: the same code,
   the same settings, the same initial values. We check whether the same
   numbers come out.
3. We take apart the design of the check: whether information unavailable
   in real operation gets into the test; whether the model is tested on data
   it was trained on; whether periods and groups are separated correctly.
4. We test behavior on deliberately empty data: we substitute data where
   no relationship exists by construction and see whether the procedure
   "finds" a pattern there. How many times it errs is recorded as a number,
   together with the number of attempts.
5. We compare against simple rules: "tomorrow as today", "tomorrow as the
   same day of last week". If a complex model is no better than a simple
   rule, that is also a result.
6. We write the report and, separately, the list of what we did not check.

## 5. What you get

- A one-page report in plain language: what was checked, what came out,
  what to do next.
- A list of verified claims with an outcome for each.
- An inventory of evidence: which code, which settings, which data, which
  control runs. Each file carries a checksum so that anyone can make sure
  it has not changed.
- A separate list of limitations: what remains unchecked and where the
  conclusion must not be applied.
- A machine-readable part in JSON - if your systems or your AI assistants
  will read it.

Everything except closed data can be shown to a third party.

## 6. What we need from you

- One claim to be verified, in a single sentence.
- A description of the process: how model variants are produced, how the best
  one is selected, by which rule a result is considered acceptable.
- Computation settings, initial values, library versions, a link
  to the saved version of the code.
- Data: a depersonalized fragment, or a run on your side.
- What in the data depends on what: time, groups (different objects,
  substations, batches), seasonality, time zone.

Desirable: run logs, the history of rejected variants, known failures.
If some of this is missing, the work is still possible, but part of the
conclusions will remain in the "not enough data" status.

## 7. Three outcomes and what they mean

| In the report for a human | In the machine file | What it means |
|---|---|---|
| Confirmed | PASS | The pre-recorded conditions are met within the stated bounds |
| Not confirmed | FAIL | A mandatory condition is violated, or a specific error is found |
| Not enough data | INCONCLUSIVE | Data, access, or precision of the check is missing; or the method does not apply to the task |

For the last two outcomes we always state the reason: little data, no access,
the environment does not reproduce, the evidence contradicts itself, the task
is outside the domain of the method, or a substantive reason - for example,
the relationship is indistinguishable from random noise.

Two important clarifications. "Confirmed" does not mean "the model is good".
It means: one specific claim survived one specific check within specific
bounds, and the bounds are written next to it. And the reverse: if we found
no errors, that is not proof of their absence - we write exactly what we
checked and with what sensitivity.

## 8. What we do not do and do not promise

- We do not train or improve the model, and we do not install monitoring.
- We do not explain the physics of battery wear and do not analyze the design
  of a power system - that is the work of a domain specialist.
- We do not issue a certificate and do not replace mandatory conformity
  assessment.
- We do not promise that the model will not break in the future.
- We do not assert cause-and-effect relationships.
- We do not estimate your monetary damage for you. We can show which decisions
  the found defect affects; the loss estimate is yours.

## 9. Price and timeline

Reference: 800-1200 EUR for the verification of one claim. The exact price
is fixed after we see the volume and availability of the materials.
Timeline: 3-5 business days from the moment the complete set of materials
is received.

Included: fixing the criteria, one verification cycle, the report, the list
of limitations, one round of clarifications.
Not included: repeat runs after the model or the data changes, model
improvement, work on several models at once.

Liability is limited to the cost of the work. The report is an engineering
opinion, not a certificate and not a guarantee.

## 10. Confidentiality

A non-disclosure agreement is signed before the data is transferred.
A run on your side is possible: the data does not leave your perimeter.
Your data is not passed to external AI services without written consent.
We do not request passwords or access to your working systems.
In the report, every artifact is marked: open, for you only, or closed
(the contents under the agreement; from the outside only checksums are
visible).
The contract form and the payment method are agreed before an offer is
issued. If we cannot agree - we decline the work instead of looking for
a workaround.

## 11. The limits of our competence, honestly

- One person performs the check and confirms it. For paid work an external
  reviewer is engaged; any conflict of interest is stated in the report.
- No independent replication by a third party has taken place yet. All
  current results are the author's, and every report says so.
- Before the first paid verification we publish a test of the procedure itself:
  we run it on examples with pre-planted errors and on deliberately clean
  ones, and show how many errors were missed and how many clean examples
  were rejected in error - with the number of attempts and an uncertainty
  bound. Until this test is published, no paid verifications are performed.
  We call this published test the verifier track record.
- We are not physicists and not power engineers. Conclusions about the
  subject domain belong to a domain specialist.
- An open example of our work: [github.com/sensus-stoa/permutation-test-ml](https://github.com/sensus-stoa/permutation-test-ml). You can also see there
  where the method does not work.

## 12. How to start

Write which claim about your model you want to verify and what you can
provide. We will answer whether the task fits and what is needed for
an estimate. If it does not fit - we will say so directly.

Contact: beattle1984@gmail.com, [profile].
Disputes and ambiguous situations are decided by a person, not
by automation.

---

The short version of the service (one-pager): `one-pager.typ` -> `one-pager.pdf`,
its text also lives in `README.md`. Text and number edits are the owner's call.
