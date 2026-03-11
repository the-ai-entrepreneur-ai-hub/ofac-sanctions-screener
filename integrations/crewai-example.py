"""Use OFAC Sanctions Screener as a CrewAI tool via Apify MCP Server."""
from crewai import Agent, Task, Crew
from crewai_tools import ApifyActorTool

sanctions_tool = ApifyActorTool(
    actor_id="george.the.developer/ofac-sanctions-screener",
    name="OFAC Sanctions Screener",
    description="Screen entities against the US OFAC SDN sanctions list. Input: queries (list of names), matchThreshold (0-100)."
)

compliance_agent = Agent(
    role="Compliance Analyst",
    goal="Screen business partners against sanctions lists before contract signing",
    backstory="Expert in trade compliance and sanctions screening",
    tools=[sanctions_tool],
)

screening_task = Task(
    description="Screen the following entities for OFAC sanctions: {entities}",
    expected_output="Structured sanctions screening report with risk levels for each entity",
    agent=compliance_agent,
)

crew = Crew(agents=[compliance_agent], tasks=[screening_task])
result = crew.kickoff(inputs={"entities": "Bank Melli Iran, Huawei Technologies, Apple Inc"})
print(result)
