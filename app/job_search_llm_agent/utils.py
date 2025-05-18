import functools
import logging

log = logging.getLogger(__name__)


def swallow_exceptions(fn):
    @functools.wraps(fn)
    def _safe(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            log.error("Unhandled in %s: %s", fn.__name__, exc, exc_info=True)

    return _safe
