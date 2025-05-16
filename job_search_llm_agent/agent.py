from .logging_setup import configure as _configure_log
from .utils import swallow_exceptions
from . import config  # noqa: F401 side-effect import: loads .env & checks keys
from . import fetcher, storage

_configure_log()


@swallow_exceptions
def run_once() -> None:
    posts = fetcher.fetch_job_postings(source="stub")
    # vecs = [embedder.embed(p) for p in posts]
    # vecs not persisted yet — Phase 1 will handle that
    storage.save_raw(posts)


if __name__ == "__main__":
    run_once()
