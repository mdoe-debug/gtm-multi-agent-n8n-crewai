import sys
from gtm_crew.crew import GtmCrew

PROJECT_BRIEF = {
    "company": "WE+, LLC",
    "product": (
        "AI Workforce Integration Advisory (flagship offering: the "
        "'Performance Architecture Sprint' - a 6-week engagement that "
        "audits an org's workforce, designs an AI adoption roadmap, and "
        "builds governance/ROI measurement frameworks)"
    ),
    "target_market": (
        "Small-to-mid size and mid-to-large enterprises (roughly 50-10,000 "
        "employees) undergoing AI transformation, spanning both corporate "
        "for-profit and nonprofit sectors, primarily in the US"
    ),
    "research_questions": [
        "Who are the top 5-7 direct competitors in AI workforce transformation advisory, and do they target SMB or enterprise segments differently?",
        "What pricing/engagement models do competitors use, and how do they scale pricing for smaller orgs vs. large enterprises?",
        "What are the top buyer objections to hiring an AI transformation advisor vs. building in-house, and do objections differ between SMB and enterprise buyers?",
        "What governance frameworks or maturity models are competitors using or referencing (e.g., NIST AI RMF, responsible AI frameworks)?",
        "How do competitors differentiate between for-profit and nonprofit client engagements, and between SMB and enterprise client engagements?",
        "What measurable ROI metrics do competitors claim or case-study, and are these metrics different at smaller org scale?",
        "What recent market signals suggest demand trends for this category across company sizes?",
    ],
    "constraints": {
        "budget_cap_usd": 5,
        "deadline_minutes": 15,
    },
}


def run():
    """Run the crew with the WE+, LLC project brief."""
    inputs = {"project_brief": str(PROJECT_BRIEF)}
    try:
        result = GtmCrew().crew().kickoff(inputs=inputs)
        print("\n\n===== FINAL RESULT =====\n")
        print(result)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    run()
