# OFAC Sanctions Screener — MCP / AI Agent Integration

Use the OFAC Sanctions Screener as a tool for AI agents via the [Apify MCP Server](https://docs.apify.com/platform/integrations/mcp). This lets Claude Code, CrewAI, LangChain, and other AI frameworks automatically screen entities against the OFAC SDN sanctions list.

## What is MCP?

The **Model Context Protocol (MCP)** lets AI agents discover and call external tools. The Apify MCP Server exposes Apify actors as callable tools, so an AI agent can run sanctions screening as part of an automated workflow — no custom API code needed.

## Setup: Apify MCP Server

Add this to your MCP client configuration (e.g., Claude Desktop `claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "@apify/mcp-server",
        "--actors", "george.the.developer/ofac-sanctions-screener"
      ],
      "env": {
        "APIFY_TOKEN": "YOUR_APIFY_TOKEN"
      }
    }
  }
}
```

Once configured, your AI agent can call the sanctions screener by name.

## Example: Claude Code

With the MCP server running, you can ask Claude Code directly:

```
Screen these entities against OFAC sanctions: Bank Melli Iran, Gazprombank, Apple Inc
```

Claude will automatically call the actor, wait for results, and present them.

## Example: CrewAI

```python
from crewai import Agent, Task, Crew
from crewai_tools import ApifyActorTool

# Create a sanctions screening tool
sanctions_tool = ApifyActorTool(
    actor_id="george.the.developer/ofac-sanctions-screener",
    input_schema={
        "queries": ["Bank Melli Iran", "Gazprombank"],
        "matchThreshold": 70,
        "includeAliases": True,
    },
)

# Create a compliance agent
compliance_agent = Agent(
    role="Compliance Officer",
    goal="Screen all business partners against OFAC sanctions",
    backstory="You are responsible for ensuring regulatory compliance.",
    tools=[sanctions_tool],
)

# Create a screening task
screening_task = Task(
    description="Screen these entities against OFAC SDN sanctions list and report findings.",
    agent=compliance_agent,
    expected_output="Sanctions screening report with risk levels for each entity.",
)

crew = Crew(agents=[compliance_agent], tasks=[screening_task])
result = crew.kickoff()
print(result)
```

## Example: LangChain

```python
from langchain_community.utilities import ApifyWrapper

apify = ApifyWrapper(apify_api_token="YOUR_APIFY_TOKEN")

results = apify.call_actor(
    actor_id="george.the.developer/ofac-sanctions-screener",
    run_input={
        "queries": ["Bank Melli Iran", "Gazprombank", "Apple Inc"],
        "matchThreshold": 70,
    },
    dataset_mapping_function=lambda item: item,
)

for result in results:
    print(f"{result['queryName']}: {result['riskLevel']}")
```

## Use Case: Automated KYC Pipeline

Combine the OFAC screener with other actors in a compliance pipeline:

1. **Extract entities** from documents (invoices, contracts) using an NLP actor
2. **Screen entities** against OFAC sanctions using this actor
3. **Enrich flagged entities** with corporate registry data
4. **Generate report** with risk scores and recommended actions

The MCP server makes each step a simple tool call for the AI agent.

## Links

- [Apify MCP Server docs](https://docs.apify.com/platform/integrations/mcp)
- [OFAC Sanctions Screener on Apify](https://apify.com/george.the.developer/ofac-sanctions-screener)
- [Model Context Protocol spec](https://modelcontextprotocol.io)
