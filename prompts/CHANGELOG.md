# Prompt Changelog

## v1 — Initial Prompt

Date: 2026-09-18

Initial customer-support prompt.

### Changes

- Added policy-based answering.
- Added instructions not to invent information.
- Added correctness, completeness, politeness, and clarity requirements.
- Instructed the model to answer the customer's actual question.
- Instructed the model to remain clear and concise.

### Evaluation

Test set:

- Test items: **50**
- Mean score: **4.480**
- Score distribution:
  - Score 1: **0**
  - Score 2: **0**
  - Score 3: **0**
  - Score 4: **26**
  - Score 5: **24**

### Judge Reliability

Using the 92 items with matching human labels:

- Exact agreement: **41.30%**
- Cohen's κ: **0.178**

### Performance

- Generation latency: **7.04 sec/item**
- Complete harness latency: **15.34 sec/item**
- Direct API cost: **$0**

---

## v2 — Stronger Policy Grounding

Date: 2026-09-19

### Changes

- Strengthened policy-grounding instructions.
- Added an explicit instruction to answer every part of the customer's question.
- Added an explicit instruction not to assume or reinterpret information.
- Added explicit restrictions against inventing prices, refunds, deadlines, procedures, exceptions, and guarantees.
- Added a final self-check to ensure factual claims are supported by the policy.
- Added an instruction to avoid unnecessary repetitive information.

### Reason for Change

The goal was to improve correctness and completeness while reducing unsupported assumptions and unnecessary repetition.

### Results Compared with v1

Both versions were evaluated on the same **50-item held-out test set**.

| Measure | v1 | v2 | Change |
|---|---:|---:|---:|
| Test items | 50 | 50 | — |
| Mean score | 4.480 | 4.600 | +0.120 |
| Score 1 | 0 | 0 | — |
| Score 2 | 0 | 0 | — |
| Score 3 | 0 | 0 | — |
| Score 4 | 26 | 20 | -6 |
| Score 5 | 24 | 30 | +6 |
| Changed scores | — | 10 | — |
| Unchanged scores | — | 40 | — |

The v2 mean score increased by **0.120 points**. Six more test items received a score of 5, while six fewer received a score of 4.

### Judge Reliability

Using the same 92 resolved human-reference items:

| Measure | v1 | v2 | Change |
|---|---:|---:|---:|
| Agreements | 38 | 43 | +5 |
| Disagreements | 54 | 49 | -5 |
| Exact agreement | 41.30% | 46.74% | +5.44 pp |
| Cohen's κ | 0.178 | 0.202 | +0.024 |

The v2 judge showed higher agreement with the resolved human reference.

### Performance

The prompt improvement also increased inference time:

| Measure | v1 | v2 |
|---|---:|---:|
| Generation latency | 7.04 sec/item | 9.47 sec/item |
| Judge latency | 8.30 sec/item | 12.05 sec/item |
| Complete harness latency | 15.34 sec/item | 21.52 sec/item |
| Direct API cost | $0 | $0 |

### Conclusion

v2 produced a higher mean score on the held-out test set and improved judge/reference agreement. However, it also increased inference latency. The results demonstrate a trade-off between measured response quality and local inference performance.