# ADR-001 — ClaimsCopilot: model and deployment decision

| | |
|---|---|
| **Version** | v1 *(change to v2 in the second file)* |
| **Status** | Proposed |
| **Author** | *your name* · Team *x* |
| **Date** | *today* |

> **What changed and why** *(v2 only — delete this box in v1)*
> *2–3 lines: what the update was, and which parts of this ADR you changed.*

---

## 1. Context
*Two or three lines in your own words: what problem, for whom, and the main constraints (data, budget, skills, timeline).*
Bharat Suraksha Insurance wants to build ClaimsCopilot to automate claim summarization, policy Q&A, and customer-letter drafting, reducing the manual effort for 3,200 claims staff and agents.

## 2. Decision drivers
*Rank the top 4. Examples: data residency · cost per month · time to launch · quality · team skills · latency · vendor lock-in.*

1. data residency
2. cost per month
3. time to launch
4. quality

## 3. Options considered

| Option (path + pay model + model) | Pros | Cons |
|---|---|---|
| **A.** | | | Public cloud dedicated
| **B.** | | | Pay as you go
| **C.** | | | propratory

## 4. Decision
**We will use** *(path)* **with** *(pay model)* **and** *(model(s) per workload)* **in** *(region)* **because** *(top 2 reasons)*.
We will use public cloud dedicated with pay as you go and propratory per workload in india becuase 
    avaliability 
    performence

| Workload | Model | Why |
|---|---|---|
| 1 · Claim summary | | | - propratory -
| 2 · Policy Q&A | | | propratory with RAG - Security 
| 3 · Customer letters | | | propratory - 

## 5. Data residency & protection
*Region, private connectivity, who can see prompts, what is logged.*

## 6. Cost estimate (per month)

| Workload | Calculation | USD / month |
|---|---|---:|
| 1 · Summary | 40,000 × 25,000 input + 40,000 × 800 output = 1,000M input + 32M output tokens | ~$2,256 |
| 2 · Q&A | 2,500 × 30 × 4,000 input + 2,500 × 30 × 400 output = 300M input + 30M output tokens | ~$210 |
| 3 · Letters | 15,000 × 1,500 input + 15,000 × 500 output = 22.5M input + 7.5M output tokens | ~$26 |
| **Total** | **1,322.5M input + 69.5M output tokens** | **~$2,492** |

*Fits the USD 4,000 budget?* Yes / No — *what would you do about it?*
Yes, we gave soltion with in budget and saving around 1500 USD per month



## 7. Consequences
- **Easier:**
- **Harder:**
- **Risks and how we reduce them:**
- **How we change our mind later (exit plan):**

## 8. Rejected options — in one line each
-
-
