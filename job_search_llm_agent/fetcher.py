import logging

log = logging.getLogger(__name__)


def fetch_job_postings(*, source: str) -> list[str]:
    """Placeholder: return raw postings from the requested source."""
    log.info("Fetching from %s (stub)", source)
    return []
