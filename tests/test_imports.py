import importlib
import pytest


@pytest.mark.parametrize(
    "module",
    [
        "job_search_llm_agent.fetcher",
        "job_search_llm_agent.embedder",
        "job_search_llm_agent.storage",
        "job_search_llm_agent.agent",
    ],
)
def test_imports(module):
    importlib.import_module(module)
