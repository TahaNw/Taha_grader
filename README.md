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
Install Ollama.
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