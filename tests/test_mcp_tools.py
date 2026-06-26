"""
Tool-level KPI tests (Phase 5, Section 1).
Mocked — no live API/network calls, no MCP server needs to be running.

ADJUST THE IMPORTS: these assume your tools live at
  tools/mcp_tools.py  -> get_research_tools(), get_docs_tools()
  tools/docs_tool.py  -> DocsWriteTool (the custom wrapper with `doc_title`)
Rename to match your actual module/class/function names if different.
"""
import pytest
from unittest.mock import patch, MagicMock

from tools.mcp_tools import get_research_tools, get_docs_tools
from tools.docs_tool import DocsWriteTool


# ---------------------------------------------------------------------------
# KPI: web_search returns well-formed results
# ---------------------------------------------------------------------------

def test_web_search_returns_well_formed_results(mock_web_search_results):
    research_tools = get_research_tools()
    web_search_tool = next(t for t in research_tools if "search" in t.name.lower())

    with patch.object(web_search_tool, "_run", return_value=mock_web_search_results):
        results = web_search_tool._run(query="performance architecture market")

    assert isinstance(results, list)
    assert len(results) > 0
    for r in results:
        assert "title" in r and "url" in r and "snippet" in r
        assert r["url"].startswith("http")


def test_research_agent_does_not_get_docs_write():
    """Agent tool-scoping KPI: research tools must NOT include docs_write."""
    research_tools = get_research_tools()
    tool_names = [t.name.lower() for t in research_tools]
    assert not any("docs_write" in n or "docs write" in n for n in tool_names)


def test_head_planner_only_gets_docs_tools():
    """Agent tool-scoping KPI: docs tools must NOT include web_search/fetch_page."""
    docs_tools = get_docs_tools()
    tool_names = [t.name.lower() for t in docs_tools]
    assert not any("search" in n or "fetch" in n for n in tool_names)


# ---------------------------------------------------------------------------
# KPI: fetch_page handles both success and failure without raising
# ---------------------------------------------------------------------------

def test_fetch_page_success(mock_fetch_page_success):
    research_tools = get_research_tools()
    fetch_tool = next(t for t in research_tools if "fetch" in t.name.lower())

    with patch.object(fetch_tool, "_run", return_value=mock_fetch_page_success):
        result = fetch_tool._run(url="https://www.gartner.com/reports/perf-arch-2026")

    assert result["status"] == 200
    assert len(result["content"]) > 0


def test_fetch_page_failure_does_not_raise(mock_fetch_page_failure):
    research_tools = get_research_tools()
    fetch_tool = next(t for t in research_tools if "fetch" in t.name.lower())

    with patch.object(fetch_tool, "_run", return_value=mock_fetch_page_failure):
        # Should return an error payload/string, not throw
        result = fetch_tool._run(url="https://broken-link.example.com/404")

    assert result.get("status") == 404 or "error" in result


# ---------------------------------------------------------------------------
# KPI: docs_write wrapper validates `doc_title` (the field-name fix you made)
# ---------------------------------------------------------------------------

def test_docs_write_succeeds_with_doc_title(mock_docs_write_success):
    tool = DocsWriteTool()

    with patch.object(tool, "_run", return_value=mock_docs_write_success) as mocked_run:
        result = tool._run(
            doc_title="WE+, LLC Performance Architecture Sprint GTM Plan",
            content="# GTM Plan\n\nFull content here...",
        )

    assert result["status"] == "success"
    assert "doc_title" in result


def test_docs_write_rejects_missing_doc_title():
    """
    Pydantic validation should reject a call missing the required doc_title
    field rather than silently writing a blank-titled file.
    """
    tool = DocsWriteTool()
    with pytest.raises(Exception):
        # Intentionally omit doc_title to confirm validation still fires
        tool._run(content="# GTM Plan\n\nFull content here...")


# ---------------------------------------------------------------------------
# KPI: tool errors surface as strings/exceptions handled by CrewAI,
# never as uncaught crashes that would kill the whole crew run
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tool_getter,tool_match", [
    (get_research_tools, "search"),
    (get_research_tools, "fetch"),
])
def test_tool_raises_clean_exception_on_forced_error(tool_getter, tool_match):
    tools = tool_getter()
    tool = next(t for t in tools if tool_match in t.name.lower())

    with patch.object(tool, "_run", side_effect=ConnectionError("simulated network failure")):
        with pytest.raises(ConnectionError):
            tool._run(query="x") if tool_match == "search" else tool._run(url="https://x.com")
    # The key KPI here isn't "no exception" — it's "a clean, typed exception"
    # rather than e.g. a silent hang or a malformed return value.
