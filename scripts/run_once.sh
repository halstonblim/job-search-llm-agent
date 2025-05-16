#!/usr/bin/env bash
set -euo pipefail
source "$(conda info --base)"/etc/profile.d/conda.sh
conda activate job-agent
pip install --editable .
python -m job_search_llm_agent.agent 