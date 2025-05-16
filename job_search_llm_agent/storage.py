"""Storage utilities for saving raw job postings."""

import json
import logging
from pathlib import Path

log = logging.getLogger(__name__)

DATA_DIR: Path = Path("data")


def save_raw(posts: list[str], fname: str = "raw.json") -> None:
    """Save raw job postings to a JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / fname
    path.write_text(json.dumps(posts, indent=2))
    log.info("Saved %d postings to %s", len(posts), path)
