"""
Shared fixtures for Phase 5 mocked testing.

IMPORTANT: This file makes assumptions about function/class names in your
existing tools/mcp_tools.py and tools/docs_tool.py since I haven't seen the
exact source. Adjust the `import` lines and the `monkeypatch.setattr` targets
to match your real names — everything else (mock shapes, assertions) should
work unchanged once the import paths line up.
"""
import pytest
from unittest.mock import MagicMock


# ---------------------------------------------------------------------------
# Mocked tool-level return payloads
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_web_search_results():
    """Shape returned by a healthy web_search() call."""
    return [
        {
            "title": "Performance Architecture Market Report 2026",
            "url": "https://www.gartner.com/reports/perf-arch-2026",
            "snippet": "The performance architecture sprint market is projected to grow...",
        },
        {
            "title": "Competitive Landscape: GTM Sprint Tools",
            "url": "https://www.forrester.com/gtm-sprint-landscape",
            "snippet": "Key players include...",
        },
        {
            "title": "Buyer Behavior in B2B Sprint Services",
            "url": "https://hbr.org/buyer-behavior-sprint",
            "snippet": "Decision makers prioritize speed and measurable ROI...",
        },
    ]


@pytest.fixture
def mock_fetch_page_success():
    return {
        "url": "https://www.gartner.com/reports/perf-arch-2026",
        "status": 200,
        "content": "Full page text content here, several paragraphs of market data...",
    }


@pytest.fixture
def mock_fetch_page_failure():
    return {
        "url": "https://broken-link.example.com/404",
        "status": 404,
        "error": "Page not found",
    }


@pytest.fixture
def mock_docs_write_success():
    return {
        "status": "success",
        "doc_title": "WE+, LLC Performance Architecture Sprint GTM Plan",
        "path": "/home/azureuser/mcp-research-server/WE+,_LLC_Performance_Architecture_Sprint_Go-To-Market_Plan.md",
    }


# ---------------------------------------------------------------------------
# Mocked LLM completion for CrewAI agent calls (so scenario tests don't
# burn API tokens). Patches whatever LLM client crew.py instantiates.
# ---------------------------------------------------------------------------

@pytest.fixture
def mock_llm_response_factory():
    """
    Returns a callable that builds a fake LLM response string given a task
    name, so each mocked task in the crew gets distinct, non-empty content
    instead of every task returning the same canned string.
    """
    def _make(task_name: str, brief: dict) -> str:
        company = brief.get("company_name", "TestCo")
        product = brief.get("product", "TestProduct")
        return (
            f"[MOCKED OUTPUT for task={task_name}] "
            f"Analysis for {company} / {product}. "
            f"This is deterministic placeholder content with enough length "
            f"to pass non-empty-output checks. Source: https://example.com/{task_name}"
        )
    return _make


@pytest.fixture
def sample_briefs():
    """Three distinct GTM input briefs to drive scenario tests."""
    return [
        {
            "company_name": "WE+, LLC",
            "product": "Performance Architecture Sprint",
            "industry": "B2B consulting / org performance",
            "target_market": "Mid-market companies, 200-2000 employees",
        },
        {
            "company_name": "Northwind Robotics",
            "product": "Warehouse Pick-Assist Module",
            "industry": "Industrial automation / robotics",
            "target_market": "3PL and e-commerce fulfillment centers",
        },
        {
            "company_name": "Lumen Health Analytics",
            "product": "Clinical Risk Scoring API",
            "industry": "Healthcare SaaS",
            "target_market": "Mid-size hospital systems and payer networks",
        },
    ]
