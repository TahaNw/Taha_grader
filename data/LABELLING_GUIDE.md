# Customer Support Replies — Labelling Guide

## 1. Task

We evaluate AI-generated customer support replies.

Each evaluation contains:

- A customer message
- A company policy
- An AI-generated support reply

The labeller must determine how well the reply answers the customer's request while following the provided policy.

The **company policy is the only source of truth**.

---

## 2. What Makes a Good Reply?

A good customer support reply should satisfy four criteria.

### A. Correctness

The response must be factually consistent with the provided policy.

The response must not:

- contradict the policy
- invent rules
- invent prices
- invent deadlines
- invent refunds or compensation
- promise something that the policy does not allow
- provide unsupported procedures or guarantees

If the policy does not contain enough information to answer a question, the reply should acknowledge that rather than inventing an answer.

### B. Completeness

The response should address the important parts of the customer's request.

Important information from the policy should be included when it is necessary to answer the customer.

However, **not every sentence from the policy needs to be repeated**. Only information relevant to the customer's request should affect the completeness score.

### C. Politeness

The response should be respectful and professional.

The response should not:

- insult the customer
- blame the customer unnecessarily
- use aggressive language
- use inappropriate language

Minor differences in tone should not strongly affect the score if the response remains professional.

### D. Clarity

The response should be easy for the customer to understand.

It should:

- directly answer the customer's question
- use understandable language
- avoid unnecessary confusion
- avoid unnecessary repetition

A concise answer can receive the highest score if it contains everything necessary.

---

# 3. Overall Score

Use a score from 1 to 5.

## Score 5 — Excellent

The response is correct, complete, polite, and clear.

It answers the customer's request using the policy without introducing unsupported information.

Minor stylistic differences do not prevent a score of 5.

**Example:**

The policy says duplicate charges are refundable within 5–7 business days, and the reply correctly explains both the refund and the processing time.

---

## Score 4 — Good

The response is mostly correct and useful.

There is a **minor omission or small issue**, but the customer still receives an adequate answer.

Examples:

- omits a secondary but relevant detail
- slightly unclear wording
- minor stylistic issue
- answers the main question but does not include one useful policy detail

The response must not contain a significant false claim.

---

## Score 3 — Acceptable

The response is partially useful but has a **noticeable problem**.

Examples:

- misses an important part of the customer's request
- provides an incomplete answer
- contains a noticeable clarity problem
- gives correct information but fails to explain an important condition
- handles only part of a multi-part question

There should be **no major contradiction or serious invented policy information**.

Use 3 when the response is still somewhat useful but clearly falls short of a good answer.

---

## Score 2 — Poor

The response has a **significant problem** that makes it substantially less useful.

Examples:

- important information is incorrect
- major policy information is missing
- the response does not properly address the customer's problem
- an important unsupported claim is introduced
- the response gives partially incorrect instructions

The response may contain some correct information, but the problem is serious enough that the customer could be misled or left without an adequate solution.

---

## Score 1 — Very Poor

The response is substantially incorrect or unusable.

Examples:

- directly contradicts the policy
- invents important information
- gives clearly incorrect instructions
- makes an unsupported promise that materially affects the customer
- completely fails to address the customer's request

Use 1 when the response is fundamentally unreliable or unusable.

---

# 4. Important Labelling Rules

### Rule 1 — Use the policy as the source of truth

Do not use personal knowledge to decide whether a statement is correct.

Only information supported by the provided policy should be considered authoritative.

If something is not stated in the policy, do not assume that it is true.

### Rule 2 — Different wording can still be correct

Two answers do not need to use the same words.

If two responses communicate the same correct information, both can receive a high score.

### Rule 3 — Do not punish concise answers

A short response can receive a 5 if it contains all information necessary to solve the customer's problem.

Do not require the answer to repeat the entire policy.

### Rule 4 — Do not reward unnecessary length

Longer answers should not automatically receive higher scores.

Unnecessary repetition does not improve the score.

### Rule 5 — Penalize invented information

If the response introduces a policy, price, deadline, refund, compensation, procedure, or promise that is not supported by the provided policy, reduce the score according to how important the invented information is.

### Rule 6 — Distinguish missing information from incorrect information

A response that omits a minor detail may be a **4**.

A response that omits an important part of the customer's request may be a **3 or 2**, depending on how much the omission affects the usefulness of the answer.

A response that provides information that contradicts the policy is generally more serious and should receive a lower score.

### Rule 7 — Evaluate the whole reply

Do not assign a low score because of one minor wording issue if the overall answer is correct and useful.

Likewise, do not assign a high score simply because the response is fluent or polite if it contains an important policy violation.

---

# 5. Labelling Procedure

Each item must be labelled independently by two people.

Each labeller records:

- Overall score: 1–5
- Short reason explaining the main reason for the score

Labellers should not discuss their decisions before submitting their individual labels.

After both labels are collected:

1. Compare the two scores.
2. Record agreements and disagreements.
3. Investigate disagreements to identify unclear cases or weaknesses in the guide.
4. Do not automatically change one label to match the other.

The purpose of independent labelling is to measure how consistently the guide can be applied.

---

# 6. Examples

## Example 1 — Excellent

### Customer

"I was charged twice for my order. Can I get the extra charge refunded?"

### Policy

"Duplicate charges are eligible for a refund. Refunds are processed within 5–7 business days."

### Reply

"Yes. The duplicate charge is eligible for a refund. Once processed, the refund should arrive within 5–7 business days."

### Label

Score: 5

Reason:

"The reply correctly explains that the duplicate charge can be refunded and provides the correct processing time."

---

## Example 2 — Minor Omission

### Customer

"I was charged twice for my order. Can I get the extra charge refunded?"

### Policy

"Duplicate charges are eligible for a refund. Refunds are processed within 5–7 business days."

### Reply

"Yes, the duplicate charge can be refunded."

### Label

Score: 4

Reason:

"The main question is answered correctly, but the response omits the 5–7 business day processing time."

---

## Example 3 — Important Incompleteness

### Customer

"I was charged twice for my order. Can I get the extra charge refunded, and how long will it take?"

### Policy

"Duplicate charges are eligible for a refund. Refunds are processed within 5–7 business days."

### Reply

"Yes, the duplicate charge can be refunded."

### Label

Score: 3

Reason:

"The reply correctly addresses the refund but fails to answer the customer's question about the processing time."

---

## Example 4 — Incorrect

### Customer

"I was charged twice for my order. Can I get the extra charge refunded?"

### Policy

"Duplicate charges are eligible for a refund. Refunds are processed within 5–7 business days."

### Reply

"Unfortunately, duplicate charges cannot be refunded."

### Label

Score: 1

Reason:

"The response directly contradicts the policy."

---

## Example 5 — Invented Information

### Customer

"I was charged twice for my order. Can I get the extra charge refunded?"

### Policy

"Duplicate charges are eligible for a refund. Refunds are processed within 5–7 business days."

### Reply

"Yes. We will refund the duplicate charge immediately, and you will receive a €20 compensation for the inconvenience."

### Label

Score: 2

Reason:

"The refund is supported by the policy, but the immediate processing and €20 compensation are invented."

---

# 7. Borderline Cases

When uncertain between two scores:

1. Check the policy again.
2. Identify exactly what is wrong or missing.
3. Determine whether the issue affects correctness, completeness, politeness, or clarity.
4. Consider how important the issue is to the customer's actual request.
5. Use the score definitions above rather than comparing the response with another response.
6. Record a short reason explaining the decision.

### General rule for borderline scores

Use:

- **4** when the answer is good but has a minor issue.
- **3** when the answer is useful but has a noticeable problem or important omission.
- **2** when the problem is significant and materially reduces the usefulness or reliability of the answer.
- **1** when the answer is fundamentally incorrect, contradictory, or unusable.

Do not lower a score simply because another labeller might choose differently.

When repeated disagreements occur around the same type of case, update this guide with a concrete example rather than silently changing labels.