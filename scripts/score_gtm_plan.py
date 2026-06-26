#!/usr/bin/env python3
"""
Phase 5, Section 3 — Output-Quality KPI scorer.

Run this directly against the REAL generated GTM plan (no mocks, no API
calls, just text analysis):

    cd ~/gtm_crew
    python scripts/score_gtm_plan.py \
        --plan "/home/azureuser/mcp-research-server/WE+,_LLC_Performance_Architecture_Sprint_Go-To-Market_Plan.md" \
        --company "WE+, LLC"

Exits 0 if all KPIs pass, 1 if any fail (so you can wire it into a CI step
or your submission checklist script too).
"""
import argparse
import re
import sys
from collections import Counter
from urllib.parse import urlparse

REQUIRED_SECTIONS = [
    "ideal customer profile",
    "value proposition",
    "messaging",
    "channel",
    "launch plan",
    "pricing",
    "risk",
]

PLACEHOLDER_PATTERNS = [r"\{\{.*?\}\}", r"\bTODO\b", r"Lorem ipsum", r"\[INSERT.*?\]"]

MIN_WORD_COUNT = 800
MIN_UNIQUE_DOMAINS = 3
WORDS_PER_CITATION_TARGET = 150  # i.e. expect >=1 citation per ~150 words


def load_plan(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def check_structural_completeness(text: str):
    lower = text.lower()
    found = [s for s in REQUIRED_SECTIONS if s in lower]
    # allow a couple of synonyms
    if "kpi" in lower or "metrics" in lower:
        if "timeline" not in found:
            found.append("timeline")
    if "go-to-market strategy" in lower and "gtm strategy" not in found:
        found.append("gtm strategy")
    passed = len(set(found)) >= 6
    return passed, f"{len(set(found))}/7 required sections found: {sorted(set(found))}"


def extract_urls(text: str):
    return re.findall(r"https?://[^\s\)\]\>\"']+", text)


def check_citation_coverage(text: str):
    urls = extract_urls(text)
    word_count = len(text.split())
    expected_min_citations = max(1, word_count // WORDS_PER_CITATION_TARGET)
    passed = len(urls) >= expected_min_citations
    return passed, f"{len(urls)} citations found, expected >= {expected_min_citations} for {word_count} words"


def check_source_diversity(text: str):
    urls = extract_urls(text)
    domains = {urlparse(u).netloc for u in urls}
    passed = len(domains) >= MIN_UNIQUE_DOMAINS
    return passed, f"{len(domains)} unique domains found: {sorted(domains)}"


def check_length(text: str):
    word_count = len(text.split())
    passed = word_count >= MIN_WORD_COUNT
    return passed, f"{word_count} words (min {MIN_WORD_COUNT})"


def check_no_placeholders(text: str):
    hits = []
    for pattern in PLACEHOLDER_PATTERNS:
        hits.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    passed = len(hits) == 0
    return passed, f"{len(hits)} placeholder/template strings found: {hits[:5]}"


def check_company_name_present(text: str, company: str):
    passed = company.lower() in text.lower()
    return passed, f"'{company}' {'found' if passed else 'NOT FOUND'} in document"


def main():
    parser = argparse.ArgumentParser(description="Score a generated GTM plan against Phase 5 KPIs.")
    parser.add_argument("--plan", required=True, help="Path to the generated .md GTM plan")
    parser.add_argument("--company", required=True, help="Company name expected to appear in the plan")
    args = parser.parse_args()

    text = load_plan(args.plan)

    checks = [
        ("Structural completeness", check_structural_completeness(text)),
        ("Citation coverage", check_citation_coverage(text)),
        ("Source diversity", check_source_diversity(text)),
        ("Length/depth", check_length(text)),
        ("No placeholder leakage", check_no_placeholders(text)),
        ("Company name present", check_company_name_present(text, args.company)),
    ]

    print(f"\n=== Phase 5 KPI Scorecard — {args.plan} ===\n")
    all_passed = True
    for name, (passed, detail) in checks:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"[{status}] {name}: {detail}")

    print("\n" + ("ALL KPIs PASSED" if all_passed else "ONE OR MORE KPIs FAILED"))
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
