from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, task, crew
from .tools.mcp_tools import get_research_tools
from .tools.docs_tool import DocsWriteTool


@CrewBase
class GtmCrew:
    """WE+, LLC GTM research and planning crew."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def head_planner(self) -> Agent:
        return Agent(
            config=self.agents_config["head_planner"],
            tools=[DocsWriteTool()],
            verbose=True,
        )

    @agent
    def research_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["research_agent"],
            tools=get_research_tools(),
            verbose=True,
        )

    @agent
    def analyst_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["analyst_agent"],
            verbose=True,
        )

    @agent
    def strategy_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["strategy_agent"],
            verbose=True,
        )

    @task
    def plan_research(self) -> Task:
        return Task(config=self.tasks_config["plan_research"])

    @task
    def gather_evidence(self) -> Task:
        return Task(config=self.tasks_config["gather_evidence"])

    @task
    def analyze_market(self) -> Task:
        return Task(config=self.tasks_config["analyze_market"])

    @task
    def draft_gtm_plan(self) -> Task:
        return Task(config=self.tasks_config["draft_gtm_plan"])

    @task
    def export_doc(self) -> Task:
        return Task(config=self.tasks_config["export_doc"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
