# GTM Multi-Agent Research & Planning System (n8n + CrewAI)

A multi-agent system that automates market research and go-to-market (GTM) 
planning for WE+, LLC's Performance Architecture Sprint offering. Implemented 
in two parallel tracks — **n8n** and **CrewAI** — both connected to a shared 
MCP (Model Context Protocol) research server.

## Demo & Screenshots
📊 [View workflow screenshots & demo (Gamma)](https://gamma.app/docs/GTM-Stratgey-Screenshots--oji6cakc4hqyhke)

## Architecture

- **MCP Server** (`~/mcp-research-server`): exposes `web_search` (via SerpAPI), 
  `fetch_page` (with local caching), and `docs_write` tools to both implementations.
- **CrewAI implementation** (`src/gtm_crew/`): 4 agents — Head Planner, Research 
  Agent, Analyst Agent, Strategy Agent — chained through 5 sequential tasks 
  (plan_research → gather_evidence → analyze_market → draft_gtm_plan → export_doc).
- **n8n implementation** (`docs/n8n_workflow_export.json`): Trigger → Head Planner 
  → Research Agent → Analyst Agent → Strategy Agent → Docs Writer, using n8n AI 
  Agent nodes + an MCP Client Tool node pointing at the same MCP server.

## Setup

### CrewAI
\`\`\`bash
cd gtm_crew
uv sync
uv run gtm_crew
\`\`\`

### n8n
\`\`\`bash
n8n start
# import docs/n8n_workflow_export.json via the n8n editor UI
\`\`\`

### MCP Server
\`\`\`bash
cd mcp-research-server
uv sync
uv run server.py
\`\`\`

## Testing & KPIs

Tests live in \`tests/\` and run via:
\`\`\`bash
uv run pytest tests/ -v
\`\`\`

KPI rubric (\`scripts/score_gtm_plan.py\` + \`PHASE5_KPI_RUBRIC.md\`) checks:
- ✅ Coverage — research questions answered with linked sources
- ✅ Source quality — citation coverage, source diversity, 0% broken links
- ✅ Latency — brief to drafted GTM document
- ✅ Strategy quality — structural completeness (ICPs, value prop, messaging, channels)
- ✅ Reproducibility — consistent facts across runs
- ✅ Cost efficiency — within budget cap

All six KPIs are passing on the CrewAI implementation's output.

## Sample Output

A real generated GTM plan (with inline citations and a Sources section) is 
included in this repo for reference.

## n8n vs CrewAI Comparison

*Pending* — the n8n workflow has been built and connected to the shared MCP 
server but has not yet been load-tested or formally compared against the 
CrewAI implementation on cost, latency, and reliability. This section will be 
completed once comparative testing is finished.

## Google Docs Export

Programmatic Google Docs/Drive API export was attempted via service account 
and OAuth Desktop flows but was blocked by Drive storage quota limits on 
personal (non-Workspace) accounts. \`docs_write\` currently exports to local 
markdown by design; the sample Google Docs deliverable was created by manually 
pasting generated output into a Google Doc.
