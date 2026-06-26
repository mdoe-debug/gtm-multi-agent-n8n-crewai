# Phase 5 — Testing & KPI Verification Rubric
**Project:** WE+, LLC — Multi-Agent GTM Research System (CrewAI + MCP)

This rubric defines measurable, scriptable KPIs so "it ran with no errors" becomes
"it ran with no errors AND produced a plan that meets defined quality bars."
Each KPI has: what it measures, how it's measured, and a pass threshold.

---

## 1. Tool-Level KPIs (unit tests, mocked)

| KPI | Measured by | Threshold |
|---|---|---|
| `web_search` returns well-formed results | schema check: list of dicts with `title`, `url`, `snippet` | 100% of mocked calls pass schema |
| `fetch_page` handles success + failure | mock 200 and mock timeout/404 | both paths return without raising |
| `docs_write` accepts `doc_title` field | call wrapper with valid + missing `doc_title` | valid succeeds, missing raises validation error (not silently writes blank) |
| Tool error handling | force a mocked exception in each tool | agent-facing tool returns a string error, never raises uncaught |

## 2. Agent/Task-Level KPIs (scenario tests, mocked LLM + tools)

| KPI | Measured by | Threshold |
|---|---|---|
| Task chain completes for ≥3 distinct input briefs | run crew.py with 3 different `inputs` dicts (different industries/products) | 3/3 complete without exception |
| Each task produces non-empty output | check `task.output.raw` (or equivalent) length | > 0 chars for all 5 tasks, all 3 runs |
| Agent tool-scoping respected | inspect tool calls per agent in mocked run | research_agent never calls `docs_write`; head_planner never calls `web_search`/`fetch_page` |
| No cross-task data loss | check that `gather_evidence` output appears referenced in `analyze_market` input/output | evidence count in analysis ≥ evidence count gathered (no silent drop) |

## 3. Output-Quality KPIs (scored against the generated `.md` GTM plan)

These run against the **real markdown file** (`WE+,_LLC_..._Go-To-Market_Plan.md`), not mocks — it's a static-text check, no API calls needed.

| KPI | Measured by | Threshold |
|---|---|---|
| Structural completeness | required section headers present (Executive Summary, Market Analysis, Target Segments, GTM Strategy, Pricing, Timeline/KPIs, Risks) | ≥ 6 of 7 sections present |
| Citation coverage | count of `[source]`/URL-style citations vs. count of factual/numeric claims (rough heuristic: sentences with numbers or named entities) | ≥ 1 citation per ~150 words OR ≥ 1 per major claim cluster |
| Source diversity | count of unique root domains cited | ≥ 3 unique domains |
| Length/depth | total word count | ≥ 800 words (adjust to your brief's expectation) |
| No placeholder/template leakage | search for strings like `{{`, `TODO`, `Lorem ipsum`, `[INSERT` | 0 occurrences |
| Internal consistency | product/company name from input brief appears in output | name match found |

## 4. System-Level KPIs

| KPI | Measured by | Threshold |
|---|---|---|
| End-to-end runtime | wall clock time of mocked scenario run | informational (track trend, not a hard gate) — for live run, record actual time separately |
| Reproducibility | run same input twice (mocked), diff outputs structurally | both runs produce same task sequence and section structure |
| Failure isolation | kill one mocked tool mid-run | crew either retries or fails that task without crashing other agents |

---

## How this maps to your capstone deliverables
- Sections 1–2 → `tests/test_mcp_tools.py`, `tests/test_crew_scenarios.py` (pytest, mocked, run anytime, no API cost)
- Section 3 → `scripts/score_gtm_plan.py` (run once against your real generated `.md` output — this is your evidence for the rubric submission)
- Section 4 → covered partly in scenario tests + manual note in README about the one live run's wall-clock time

Adjust numeric thresholds (word count, citation density, domain count) once you see your real plan's stats — run `score_gtm_plan.py` first to get a baseline, then decide if the bar is fair.
