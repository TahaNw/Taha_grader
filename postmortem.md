# Postmortem

## 1. Overview

The goal of this project was to build a reusable evaluation harness for a customer-support reply system. The system uses **Qwen2.5 7B locally through Ollama**, while the harness evaluates generated replies using an LLM judge and a golden dataset.

The project produced a **150-item dataset**, an automated evaluation harness, an LLM judge, prompt versions, reliability experiments, bias tests, and cost and latency measurements.

## 2. Problems Encountered

### 2.1 Human-label disagreement
Out of 150 items:
- **92 items (61.33%)** had matching labels.
- **58 items** had different labels.
- Cohen's kappa was **0.447**.
This showed that some customer-support cases can be interpreted differently even when using the same labelling guide.
The disagreements also affected judge-reliability analysis.

### 2.2 LLM judge reliability
The LLM judge did not perfectly reproduce the human reference labels.
This demonstrated that an LLM judge should not automatically be treated as ground truth. The quality of the reference labels and the consistency of the judge both affect evaluation results.

### 2.3 Position bias
The position-bias experiment showed that the judge could change its score when the positions of two answers were swapped.
Out of 150 items:
- **54 (36.00%)** were unchanged.
- **96 (64.00%)** changed.

### 2.4 Verbosity sensitivity
The verbosity experiment appended irrelevant, repetitive text to generated answers.
The results were:
- **67 (44.67%)** unchanged.
- **3 (2.00%)** increased.
- **80 (53.33%)** decreased.

### 2.5 Prompt improvement trade-off
A second system prompt was introduced to make policy grounding and completeness more explicit.
On the same 50-item test set:
- v1 mean score: **4.480**
- v1 Generation latency: **7.04 seconds/item**
- v2 mean score: **4.600**
- v2 Generation latency: **9.47 seconds/item**
This showed that prompt improvements can affect both quality measurements and computational cost.

### 2.6 Local inference latency
Running the model locally avoided external API charges but introduced significant inference time.
At 15,000 requests, the observed v2 throughput would require approximately **39.46 hours** of system generation and **50.22 hours** of judge inference.

## 3. Lessons Learned

### 3.1 Evaluation quality starts with the dataset
A large dataset is not automatically a reliable evaluation dataset.
The **61.33% human-label agreement** showed that the labelling guide and individual interpretations can still produce disagreement.

### 3.2 LLM judges need reliability testing
An LLM judge should not be treated as a perfect evaluator.
The judge achieved only **41.30% exact agreement** with the resolved human labels in v1 and **46.74%** in v2.

### 3.3 Multiple metrics provide a better picture
A single overall score would hide important evaluation problems.
The project therefore measured:
- Human-label agreement
- Cohen's kappa
- Judge/reference agreement
- Judge score distributions
- Position-dependent score changes
- Verbosity-dependent score changes
- System test-set scores
- Generation latency
- Judge latency
- Total harness latency
- Estimated workload at 100× scale

### 3.4 Prompt changes should be measured on a held-out test set
The v2 prompt increased the test-set mean from **4.480 to 4.600** while keeping the same 50-item test set.
This demonstrated the importance of keeping a stable held-out test set when comparing prompt versions. Otherwise, improvements could be confused with changes in the evaluation data.

### 3.5 Local models change the cost trade-off
Using a local model resulted in **$0 direct API cost**. However, the trade-off is computation time.

### 3.6 Reproducible structure matters
Keeping the dataset, labelling guide, prompts, changelog, harness code, analysis scripts, and results in separate version-controlled directories made it possible to reproduce experiments and compare prompt versions.

## 4. What We Would Improve

If the project were continued, the first improvement would be to strengthen the human-labelling process.

The LLM judge could also be improved by testing alternative evaluation prompts. Position-swapping could be incorporated into the evaluation process to reduce dependence on a single answer ordering.

The harness could also be optimized for faster local inference. Possible improvements include reducing unnecessary output length, improving model/inference configuration, or using a smaller model for the judge.

## 5. Conclusion

The project demonstrated that building an evaluation harness involves more than generating a single quality score.

The experiments revealed **human-label disagreement**, **limited judge/reference agreement**, **position sensitivity**, **verbosity sensitivity**, and a clear **quality-versus-latency trade-off** when changing the system prompt.

The v2 prompt achieved a higher test-set mean score than v1, increasing from **4.480 to 4.600**, while also increasing inference latency.

The main lesson is that the evaluation system itself must be evaluated. Reliable measurement requires carefully defined criteria, independent labelling, stable test data, structured outputs, judge-reliability checks, bias experiments, and transparent performance measurements.