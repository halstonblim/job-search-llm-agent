[![CI Status](https://github.com/halstonblim/job-search-llm-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/halstonblim/job-search-llm-agent/actions/workflows/ci.yml)

# Job Search LLM Agent

Phase 0 bootstrap — scaffolding for an automated job-search agent.

## Getting Started

```bash
source ./scripts/bootstrap.sh # one-liner setup
pytest -q # sanity check
```

### Secrets

1. `cp .env.example .env`
2. Fill in real keys (OpenAI, Postgres, etc.)
3. Re-run `./scripts/bootstrap.sh` if you added new deps 
