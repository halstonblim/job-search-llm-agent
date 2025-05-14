#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="job-agent"

# Check if conda is initialized
if ! command -v conda &> /dev/null; then
    echo "Error: conda is not installed or not in PATH"
    exit 1
fi

# Get conda's base directory
CONDA_BASE=$(conda info --base)
CONDA_ACTIVATE="$CONDA_BASE/etc/profile.d/conda.sh"

# Source conda's activate script
if [ -f "$CONDA_ACTIVATE" ]; then
    source "$CONDA_ACTIVATE"
else
    echo "Error: Could not find conda's activate script at $CONDA_ACTIVATE"
    exit 1
fi

# ------------------------------------------------------------------
# 1. Create or update the Conda environment from environment.yml
# ------------------------------------------------------------------
if conda env list | grep -q "^$ENV_NAME "; then
  echo "Env $ENV_NAME already exists — updating from environment.yml"
  conda env update -n "$ENV_NAME" -f environment.yml  --prune
else
  echo "Creating env $ENV_NAME from environment.yml"
  conda env create -f environment.yml
fi

# ------------------------------------------------------------------
# 2. Activate & install the repo in editable mode
# ------------------------------------------------------------------
conda activate "$ENV_NAME"
# pip install -e .

# ------------------------------------------------------------------
# 3. Set up git hooks
# ------------------------------------------------------------------
# pre-commit install

echo -e "\nBootstrap complete"