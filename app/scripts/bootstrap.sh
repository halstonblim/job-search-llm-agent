#!/usr/bin/env bash
set -euo pipefail

readonly ENV_NAME="job-agent"

error() { echo "Error: $1" >&2; return 1; }

# Conda available?
command -v conda &>/dev/null || { error "conda not found in PATH"; return 1; }

# Initialise conda
CONDA_BASE=$(conda info --base)
source "$CONDA_BASE/etc/profile.d/conda.sh" \
  || { error "Could not source $CONDA_BASE/etc/profile.d/conda.sh"; return 1; }

# Ensure environment.yml exists
[[ -f environment.yml ]] || { error "environment.yml not found"; return 1; }

# Create or update env
if conda env list | grep -qE "^$ENV_NAME[[:space:]]"; then
    echo "Updating env $ENV_NAME..."
    conda env update -n "$ENV_NAME" -f environment.yml --prune \
      || { error "Failed updating env"; return 1; }
else
    echo "Creating env $ENV_NAME..."
    conda env create -n "$ENV_NAME" -f environment.yml \
      || { error "Failed creating env"; return 1; }
fi

# Activate and install editable package
conda activate "$ENV_NAME" \
  || { error "Could not activate $ENV_NAME"; return 1; }

pip install -e ".[dev]" \
  || { error "Editable install failed"; return 1; }

# Install git hooks
pre-commit install || { error "pre-commit install failed"; return 1; }

echo "Bootstrap complete – environment '$ENV_NAME' ready."
