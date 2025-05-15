from . import fetcher, storage


def run_once() -> None:
    posts = fetcher.fetch_job_postings(source="stub")
    # vecs = [embedder.embed(p) for p in posts]
    # vecs not persisted yet — Phase 1 will handle that
    storage.save_raw(posts)


if __name__ == "__main__":
    run_once()
