# Eval Harness — Build Plan

Project #1 of the AI-application-engineer mastery ladder. The **harness** is the portfolio
piece; the task flowing through it is swappable. Build it yourself from this spec — only reach
for AI when genuinely stuck.

## Why this project first
Evaluation is the rarest, most senior-signaling skill in the AI app layer, and every later
project (RAG, agents) imports it. After this you can credibly say:
- "I can measure non-deterministic systems."
- "I validate my evaluators against human labels before trusting them."
- "I gate deploys on eval regressions in CI."

## Anchor task: support-ticket triage
Input: a customer email. Output (structured JSON):
```json
{ "category": "billing | bug | feature_request | account | other",
  "priority": "low | medium | high | urgent",
  "needs_human": true,
  "summary": "one-line summary" }
```
Chosen because it has a **deterministic** part (enums + bool → exact-match / F1) AND a **fuzzy**
part (summary → LLM-as-judge), forcing you to build both scoring families. Swap for
invoice→JSON extraction if preferred; structure is identical.

## Stack (lean for 8GB i5-8250U, no GPU)
- **Python** — lingua franca for evals/interviews
- **Pydantic** — schemas + structured-output validation
- **SQLite** — results store; zero daemon, near-zero RAM
- **Hosted APIs only** — Anthropic + OpenAI (two providers so you can compare)
- **Response cache** keyed on model+prompt+input — saves money + makes runs reproducible. Build early.
- No local models, no heavy DB. Laptop stays a thin client.

RAM discipline: lightweight vector store only if needed, hosted embeddings (no local embedding
models), close browser tabs while running.

Assume ~6–10 hrs/week. Each week ends with something that runs.

---

## Week 0 — Setup (one evening)
- Repo, virtualenv, `.env` with API keys (gitignored).
- One script calling both providers, returning structured JSON via Pydantic.
- **Cost guardrail from day one:** hard spend/token cap in config; log token usage every call.
- **Done when:** `hello.py` returns validated JSON from both providers + prints tokens & est. cost.

## Week 1 — Dataset + single-variant runner + deterministic scoring
- **Dataset format:** list of cases `{ id, input, expected }` as JSONL. ~60–80 cases. Write ~15
  by hand, generate the rest with a strong model, then **hand-correct every one** (labeling
  teaches what ground truth costs).
- **Runner:** takes a *variant* (model + prompt + params), runs over every case, captures raw
  output, parsed output, tokens, latency, cost, errors. Wrap calls in the cache.
- **Deterministic scorers:** exact-match on enums, F1/precision/recall on category,
  JSON-schema-validity rate (how often output even parses — a real reliability metric).
- **Persist everything** to SQLite: one row per (run, case, variant) with all scores + metadata.
- **Done when:** one command runs a variant over the dataset, writes scored results, and you can
  query accuracy + cost + p50/p95 latency for a variant.

> Concept: schema-validity rate. Malformed JSON 8% of the time is a production outage. Measuring
> reliability is the senior move.

## Week 2 — Multi-variant + LLM-as-judge
- **Variants as config:** define N (e.g. Haiku vs GPT-mini vs Sonnet; prompt-v1 vs v2), run all
  over the dataset in one go → a grid.
- **LLM-as-judge** for the fuzzy `summary`: a separate LLM call scoring output against a rubric
  (accurate? complete? one line? score 1–5 + reasoning), using a strong model. Structured output
  so the judge is itself scoreable. Learn pointwise vs pairwise; build pointwise first.
- **Capture cost/latency per variant** in the comparison, not just quality.
- **Done when:** one command produces a table of variants × {accuracy, schema-validity,
  judge-score, cost, p95 latency}.

> Concept: the judge is another model that can be wrong — which is why Week 3 exists.

## Week 3 — Judge validation + regression tracking (the differentiating week)
- **Judge validation:** human-label a ~20-case gold subset yourself, then measure how well the
  LLM-judge agrees with you — agreement rate + **Cohen's kappa**. Iterate the rubric until
  agreement is solid; report the number. (Lean on AI for the stats here — it teaches less to
  grind solo than the engineering does.)
- **Regression tracking:** store runs over time; add a `compare` command (two run IDs →
  per-variant deltas, flag any metric dropping past a threshold).
- **Done when:** you can state "judge agrees with humans at κ=0.x" AND one command tells you
  whether run B regressed vs run A.

> Concept: eval the evaluator. "I validated my judge against human labels before trusting it" =
> more seniority signal than 90% of candidates.

## Week 4 — Reporting + CI gate + writeup
- **Report:** clean static HTML/Markdown (variants × metrics, cost/latency, judge κ, regression
  flags). Optional Streamlit flex if you want it interactive.
- **CI integration:** run the eval on a PR via GitHub Actions; **fail the build if a key metric
  regresses** past threshold (use a small cached subset so CI is cheap/fast). This is what makes
  it *production*, not a notebook.
- **README that tells the story:** task, architecture, findings, judge-validation number.
- **Done when:** a PR triggers the eval, the report renders, the README would make a hiring
  manager nod.

## Week 5 — Optional: generalize + publish
- Make the task pluggable (swap triage for invoice extraction without touching the engine).
- Blog post: "I built an LLM eval harness — what validating the judge taught me." Compounds as
  portfolio + interview material + visibility. The judge-validation angle is under-written-about.

---

## The 6-project ladder (context)
1. **Eval harness** ← you are here
2. RAG with retrieval eval (reuses this harness)
3. Tool-using / coding agent
4. LLM gateway/infra — unfair advantage (commerce/subscriptions + payments background)
5. Fine-tuning / small-model (breadth; rent GPUs / Colab)
6. Capstone: shipped end-to-end AI product

Highest-ROI pair for me: **#1 eval + #4 gateway** (least crowded, most senior-signaling).
