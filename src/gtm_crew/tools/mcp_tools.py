import os
from mcp import StdioServerParameters
from crewai_tools import MCPServerAdapter

MCP_SERVER_DIR = os.path.join(os.path.expanduser("~"), "mcp-research-server")

server_params = StdioServerParameters(
    command="uv",
    args=["run", "--directory", MCP_SERVER_DIR, "python", "server.py"],
    env=os.environ.copy(),
)

mcp_adapter = MCPServerAdapter(server_params)


def get_research_tools():
    """Tools for agents that search/fetch but don't write docs."""
    return [t for t in mcp_adapter.tools if t.name in ("web_search", "fetch_page")]


def get_docs_tools():
    """Tools for agents that need to export documents."""
    return [t for t in mcp_adapter.tools if t.name == "docs_write"]
