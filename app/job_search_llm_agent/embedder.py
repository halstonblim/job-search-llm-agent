import logging

log = logging.getLogger(__name__)


def embed(text: str) -> list[float]:
    """Return a dummy embedding so the pipeline compiles."""
    return [0.0] * 768
