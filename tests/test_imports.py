import importlib
import pytest


@pytest.mark.parametrize(
    "module",
    [
        "src.fetcher",
        "src.embedder",
        "src.storage",
        "src.agent",
    ],
)
def test_imports(module):
    importlib.import_module(module)
