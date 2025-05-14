## Project Overview

Build a publicly‑shareable, cost‑conscious agent that automatically discovers, ranks, and delivers job postings matching your evolving profile, learns from explicit feedback, and stores artefacts to avoid redundant computation.

**Constraints / Targets**

* **Cost ceiling:** ≤ US \$10 / month (pay‑as‑you‑use)
* **Run cadence:** daily cron initially; later event‑triggered
* **Tech stack anchors:** Python, FastAPI, Fly.io, Chroma/pgvector, OpenAI or open‑source embeddings + GPT‑4o; LangGraph + MCP for agent orchestration
* **Public portfolio:** MIT‑licensed repo with clean docs + small public demo dataset
* **Start date:** 13 May 2025

---

# Phase 0 — Project Bootstrap (2 days)

### Objectives

Set up scaffolding so coding iterations are frictionless and reproducible.

### Deliverables (MVP)

* **Git repo** with PR workflow, pre‑commit hooks (black, ruff) and CI (GitHub Actions → pytest).
* **Monorepo layout**: `/app` (API & agent), `/infra` (Fly.io + Terraform), `/docs`.
* **Dockerfile + Fly.toml** pinned to Python 3.12 slim.
* **env.example** with OpenAI key placeholder.

### Stretch

* Automated dependency CVE scan (e.g. Dependabot + OSV‑Scanner).

### Tools / Services

* GitHub (free), Fly.io (free allowance), GitHub Actions minutes (<\$0.50/mo at current scale).

### Sub‑tasks

1. Initialise repo, add MIT licence.
2. Set up poetry + task runner (`taskfile`) for dev commands.
3. Write baseline unit test.
4. Push to GitHub, enable branch protection + Dependabot.
5. Provision Fly.io Postgres (Free tier, 1 GB).

### Pitfalls

* Forgetting to pin image digest → reproducibility issues.

---

# Phase 1 — Core Ingestion & Matching MVP (7 days)

### Objectives

Automatically fetch top job boards, embed postings, store vectors, email digest with signed‑link feedback.

### Deliverables (MVP)

* **Scrapers** for Greenhouse & Lever (Playwright,  retry + back‑off).
* **Embedding pipeline** using `text‑embedding‑3‑small`.
* **Vector store** (Chroma with SQLite backing inside Fly volume) OR pgvector.
* **Matching logic:** cosine similarity + hard filters (location, remote, salary floor).
* **Daily cron (Fly Machines)** calling `agent.run_daily()`.
* **Digest e‑mail** (SendGrid free tier) with MJML template and unique feedback links.

### Stretch

* Add LinkedIn Jobs API (if accepted) or SerpAPI fallback.
* Basic skill‑gap hint highlighting missing keywords.

### Tools / Services & Estimated Cost

| Service              | SKU                              | Est. Monthly Cost     |
| -------------------- | -------------------------------- | --------------------- |
| OpenAI embeddings    | 0.45 M tokens → 0.45 × \$0.00002 | ≈ \$0.01              |
| SendGrid             | Free (100 emails/day)            | \$0                   |
| Fly.io Postgres + VM | First micro VM + 1 GB PG         | ≈ \$2                 |
| Total                |                                  | ≈ \$2.01 (+ headroom) |

### Sub‑tasks

1. Build job schema & DB migrations.
2. Implement scraper classes with checkpointing.
3. Pipeline CLI (`ingest.py`) → fetch → embed → upsert.
4. Matching module + explanation string generation.
5. Email sender + minimal HTML template.
6. Feedback endpoint (`/feedback/{token}`) writing to `feedback` table.
7. Cron schedule: `fly m run --schedule "0 15 * * *" python -m app.agents.daily`.

### Pitfalls

* Rate‑limits (Greenhouse/Lever) ⇒ implement ETag caching & exponential back‑off.
* Token leakage in feedback URLs ⇒ sign with HMAC + TTL (24 h).

---

# Phase 2 — Feedback‑Aware Ranking & Dashboard (5 days)

### Objectives

Learn from user feedback, surface history, avoid duplicate embeddings.

### Deliverables (MVP)

* **Cross‑encoder re‑ranker** fine‑tuned on accumulated feedback (MiniLM‑L6 + PEFT LoRA).
* **Dash app or Streamlit** page `/history` to browse previous matches, feedback, and open links.
* **Dedup logic**: before embedding, hash job‑id; skip if already stored (<90 d).
* **Email footer** with “Open dashboard” link.

### Stretch

* Natural‑language feedback parsing (“Too senior”, “need PyTorch”) → label taxonomy.

### Tools / Services

* Hugging Face Inference Endpoints (free CPU) for fine‑tuned model OR run locally on Fly second micro (\~\$2/mo when active).
* Streamlit Community Cloud (free) if off‑platform.

### Sub‑tasks

1. Export feedback CSV to HF `datasets`.
2. Fine‑tune MiniLM with 3‑way loss (interested / not / neutral).
3. Integrate cross‑encoder score into final ranking.
4. Build lightweight dashboard with auth (password‑env var).

### Pitfalls

* Overfitting on small feedback set → keep baseline similarity as back‑off.
* Streamlit cold‑start latency on free tier.

---

# Phase 3 — Dynamic Source Discovery (3 days)

### Objectives

Automatically expand source list when recall drops.

### Deliverables (MVP)

* **LLM "source planner"**: queries GPT‑4o weekly with prompt → returns new career‑page URLs.
* **Crawler queue** persists new sources, manual approve flag.
* **Coverage monitor**: alert if \<X new matches per week.

### Stretch

* Auto‑generate scrape adapters (Trafilatura + selector hints) with human verification.

### Tools / Costs

* GPT‑4o calls: 1 call/wk × 2 K tokens ≈ \$0.03/mo.
* Store planner prompts/results in Postgres.

### Sub‑tasks

1. Build “source” table (url, last\_crawled, enabled).
2. Prompt engineering for planner (“physics PhD”, “machine learning”, etc.).
3. CLI task `python -m app.agent.plan_sources` weekly cron.
4. Manual review CLI to enable new sources.

### Pitfalls

* Planner hallucinating pay‑walled sites → whitelist domains; require manual enable.

---

# Phase 4 — Skill‑Gap Insights & Learning Recs (optional, 4 days)

### Objectives

Surface aggregated missing skills & suggest resources.

### Deliverables (MVP)

* Aggregation job counting frequency of unmatched key skills across postings.
* Email section “Popular missing skills this month: \_\_\_”.
* Simple mapping YAML skill → course/blog link.

### Stretch

* Generate custom learning path via OpenAI.

### Cost Impact

Negligible extra tokens (<\$0.05/mo).

### Pitfalls

* Noise: ensure threshold before surfacing.

---

# Phase 5 — Auto‑Apply & Form‑Fill (nice‑to‑have, 5 days)

### Objectives

Automate application submission for whitelisted companies.

### Deliverables (MVP)

* Selenium script filling Name/Email/Resume/Questions.
* UI toggle per company “auto‑apply”.

### Stretch

* PDF parsing → tailored cover letter snippet.

### Compliance

Store applied job IDs to avoid duplicate submissions.

### Pitfalls

* CAPTCHAs; site layout changes; legal risk ⇒ keep opt‑in & logs.

---

# Maintenance & Ops

* **Monitoring**: Fly metrics + Grafana Cloud free tier; alert on cron failures.
* **Back‑ups**: Nightly Postgres dump to Backblaze B2 (<\$0.01/mo).
* **Logging**: Structured JSON → Logtail free.
* **Retention Cron**: purge postings > 90 d, keep embedding row stub for dedup.

---

# Learning Checklist

| Phase | New Tech / Skill                                      |
| ----- | ----------------------------------------------------- |
| 0     | Fly.io CLI, Docker multi‑stage, GitHub Actions matrix |
| 1     | Playwright scraping, Chroma, MJML                     |
| 2     | PEFT LoRA fine‑tune, Streamlit dashboard              |
| 3     | LangGraph graph definition, MCP memory store          |
| 4     | Prompt pattern design for insight generation          |
| 5     | Selenium anti‑bot tactics                             |

---

# Total Budget Forecast (per month)

| Item                     | Baseline     | Stretch (peak)      |
| ------------------------ | ------------ | ------------------- |
| Fly compute + PG         | \$2.00       | \$4.00 (2 VMs)      |
| OpenAI embeddings        | \$0.01       | \$0.20 (10× volume) |
| GPT‑4o planner + misc    | \$0.03       | \$0.50              |
| SendGrid                 | \$0          | \$0.00              |
| Misc (back‑ups, logging) | \$0.10       | \$0.30              |
| **Total**                | **≈ \$2.14** | **≈ \$5.00**        |

> **Headroom** leaves up to \~US \$5 more for burst usage while staying under your \$10 limit.

---

## Completion Criteria per Phase

* **0**: CI green, deploy “Hello World” API on Fly.
* **1**: Receive first daily digest email with accurate matches.
* **2**: Dashboard shows match history, re‑ranking reflects feedback.
* **3**: At least one new source auto‑discovered and approved.
* **4**: Email includes missing‑skill insight; count agrees with dashboard.
* **5**: Successful auto‑application log entry for one whitelisted job.

---

## Memorised Notes

* Budget cap: \$10/mo.
* Core loop: daily cron; feedback‑aware.
* Public visibility: MIT licence, clean docs.
