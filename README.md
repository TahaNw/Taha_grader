# The Grader

An evaluation harness for measuring the quality of AI-generated customer-support replies.

The project uses **Qwen2.5 7B locally through Ollama** and evaluates generated replies against a structured golden dataset using an LLM judge.

## Task

Given:

- A customer message
- A company policy

The system generates a customer-support reply.

The reply is evaluated using four criteria:

- Correctness
- Completeness
- Politeness
- Clarity

A score from **1–5** and a short reason are produced for each item.

Exact-match evaluation is not suitable for this task because multiple differently worded replies can all be correct while a fluent response can still violate the company policy.

## Evaluation Pipeline

```text
Customer Message + Company Policy
                ↓
           Qwen2.5 7B
                ↓
         Generated Reply
                ↓
           LLM Judge
                ↓
         Score + Reason
                ↓
          JSONL Results
```

## Dataset

The golden dataset contains **150 customer-support scenarios**.

- **100 development items**
- **50 test items**
- Two independent labels per item
- Scores from 1 to 5
- Labelling guide in `data/LABELLING_GUIDE.md`

The dataset covers:

- Refunds
- Returns
- Cancellations
- Shipping and late delivery
- Damaged or incorrect products
- Payments
- Discounts
- Subscriptions
- Warranties
- Accounts and passwords
- Privacy
- Missing-information and edge cases

### Human Label Agreement

The two labelers agreed on **92 of 150 items**.

- Agreement: **61.33%**
- Disagreements: **58**
- Cohen's κ: **0.447**

The 92 items where both labelers agreed are used as the resolved human reference for judge-reliability analysis.

## Models

### System Model

- **Qwen2.5 7B**
- Runtime: **Ollama**
- Local inference
- No external API key required

### Judge

The same local model is used as an LLM judge.

The judge receives:

- Customer message
- Company policy
- Generated reply

It returns structured JSON containing:

```json
{
  "score": 1,
  "reason": "Short explanation of the score."
}
```

The score is validated using Pydantic.

## Prompt Versions

The system prompt is versioned in `prompts/`.

### v1

The baseline prompt instructs the model to:

- Follow the company policy
- Avoid invented information
- Answer the customer's question
- Include relevant policy information
- Be polite, clear, and concise

### v2

The second version adds stronger instructions for:

- Answering every part of the customer's question
- Avoiding assumptions
- Avoiding unsupported procedures, refunds, deadlines, and guarantees
- Not contradicting or reinterpreting the policy
- Checking that factual claims are supported by the policy
- Avoiding unnecessary repetition

### Test-Set Comparison

The same **50-item test set** was used for both versions.

| Measure | v1 | v2 |
|---|---:|---:|
| Test items | 50 | 50 |
| Mean score | 4.480 | 4.600 |
| Score 4 | 26 | 20 |
| Score 5 | 24 | 30 |
| Changed scores | — | 10 |
| Unchanged scores | — | 40 |

The test-set mean increased by **0.120 points** from v1 to v2.

See `prompts/CHANGELOG.md` for prompt changes.

## Judge Reliability

Judge reliability was measured against the 92 resolved human-labelled items.

| Measure | v1 | v2 |
|---|---:|---:|
| Resolved items | 92 | 92 |
| Agreements | 38 | 43 |
| Disagreements | 54 | 49 |
| Exact agreement | 41.30% | 46.74% |
| Cohen's κ | 0.178 | 0.202 |

The v2 judge achieved higher agreement with the resolved human reference than v1.

## Bias Tests

### Position Bias

The judge evaluated two answers and then evaluated the same answers with their positions swapped.

Results:

- Unchanged: **54 / 150 (36.00%)**
- Changed: **96 / 150 (64.00%)**
- Average absolute score change: **0.480**

This indicates that answer position can affect the judge's score.

### Verbosity Bias

Irrelevant repetitive text was appended to generated answers and the padded answers were re-evaluated.

Results:

- Unchanged: **67 / 150 (44.67%)**
- Increased: **3 / 150 (2.00%)**
- Decreased: **80 / 150 (53.33%)**
- Average absolute score change: **0.660**

Only 2% of scores increased after irrelevant padding, while 53.33% decreased.

## Performance and Cost

The system runs locally, so there are **no direct external API charges**.

### v1 Run

| Measure | Result |
|---|---:|
| Requests | 150 |
| Generation latency | 7.04 sec/item |
| Judge latency | 8.30 sec/item |
| Complete harness latency | 15.34 sec/item |
| LLM calls | 300 |
| Direct API cost / 1,000 requests | $0 |

At 100× the workload:

- Requests: **15,000**
- Estimated system generation time: **29.34 hours**
- Estimated judge time: **34.58 hours**

### v2 Run

| Measure | Result |
|---|---:|
| Requests | 150 |
| Generation latency | 9.47 sec/item |
| Judge latency | 12.05 sec/item |
| Complete harness latency | 21.52 sec/item |
| LLM calls | 300 |
| Direct API cost / 1,000 requests | $0 |

At 100× the workload:

- Requests: **15,000**
- Estimated system generation time: **39.46 hours**
- Estimated judge time: **50.22 hours**

These are throughput estimates, not measurements of an actual 15,000-request run.

## Project Structure

```text
the-grader/
│
├── data/
│   ├── golden.jsonl
│   └── LABELLING_GUIDE.md
│
├── harness/
│   ├── __init__.py
│   ├── config.py
│   ├── llm.py
│   ├── runner.py
│   ├── judge.py
│   ├── scorer.py
│   ├── schema.py
│   └── utils.py
│
├── prompts/
│   ├── system_v1.txt
│   ├── system_v2.txt
│   ├── judge_v1.txt
│   └── CHANGELOG.md
│
├── results/
│   ├── run_*.jsonl
│   └── ...
│
├── analysis/
│   ├── human_agreement.py
│   ├── judge_reliability.py
│   ├── position_bias.py
│   ├── verbosity_bias.py
│   ├── cost_analysis.py
│   └── compare_prompts.py
│
├── README.md
├── requirements.txt
├── .gitignore
├── postmortem.md
└── report.pdf
```

## Setup

### 1. Install Ollama

Install Ollama and make sure it is running.

Then download the model:

```bash
ollama pull qwen2.5:7b
```

### 2. Install Python dependencies

From the project root:

```bash
pip install -r requirements.txt
```

If `pip` is not available on Windows, use:

```bash
py -m pip install -r requirements.txt
```

### 3. Run the evaluation

From the project root:

```bash
py -m harness.runner
```

The harness loads the golden dataset, generates a reply for every item, sends the result to the LLM judge, and saves the results as JSONL in `results/`.

## Analysis

After running an evaluation, the analysis scripts can be used to inspect different parts of the evaluation.

Human-label agreement:

```bash
py analysis/human_agreement.py
```

Judge reliability:

```bash
py analysis/judge_reliability.py
```

Position bias:

```bash
py analysis/position_bias.py
```

Verbosity bias:

```bash
py analysis/verbosity_bias.py
```

Cost and latency:

```bash
py analysis/cost_analysis.py
```

Prompt comparison:

```bash
py analysis/compare_prompts.py
```

## Results

The final experiments showed:

- **61.33%** agreement between the two labelers
- **κ = 0.447** human-label agreement
- **41.30% → 46.74%** judge/reference exact agreement from v1 to v2
- **0.178 → 0.202** Cohen's κ for judge reliability
- **64.00%** of position-bias tests changed score
- **53.33%** of verbosity tests decreased score after irrelevant padding
- **4.480 → 4.600** test-set mean score from system v1 to v2
- **$0 direct API cost** because inference runs locally

See `report.pdf` for the full evaluation report and `postmortem.md` for problems, lessons learned, and proposed improvements.

## Reproducibility

The project keeps the following under version control:

- Golden dataset
- Labelling guide
- System prompts
- Judge prompt
- Prompt changelog
- Evaluation scripts
- Analysis scripts
- Per-item JSONL results

The test set is kept separate from the development set so that prompt changes can be evaluated on the same held-out items.

## Contributions

- **Taha Bouzahar** — Dataset preparation, labelling, evaluation harness, LLM judge, reliability and bias analysis, prompt evaluation, documentation, and report.
- **Team Member 2** — _Add contribution here._
- **Team Member 3** — _Add contribution here._
- **Team Member 4** — _Add contribution here._