# OFAC Sanctions Screener — Automated SDN List Compliance Check

[![Apify Actor](https://img.shields.io/badge/Apify-Actor-blue?logo=apify)](https://apify.com/george.the.developer/ofac-sanctions-screener)
[![Available on RapidAPI](https://img.shields.io/badge/Also%20on-RapidAPI-blue?logo=rapidapi)](https://rapidapi.com/georgethedeveloper3046/api/ofac-sanctions-screener-api)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Screen companies, individuals, vessels, and addresses against the **US Treasury OFAC SDN (Specially Designated Nationals) sanctions list** with fuzzy matching, alias detection, and confidence scoring. Enterprise-grade compliance screening for **$0.01/entity** — no contracts, no minimums.

> OFAC penalties can reach **$20 million per violation**. This actor screens your entities against the same official SDN data used by enterprise compliance tools, at a fraction of the cost.

**[Run on Apify](https://apify.com/george.the.developer/ofac-sanctions-screener)** | **[API Docs](https://docs.apify.com/api/v2)**

---

## Features

- **Official OFAC SDN Data** — Downloads directly from the US Treasury (18,000+ sanctioned entities, refreshed daily)
- **Fuzzy Matching** — Catches name variations, misspellings, and transliterations using Dice coefficient + Fuse.js
- **Alias Detection** — Matches against all known aliases (AKAs) for each sanctioned entity
- **Confidence Scoring** — 0-100% match confidence with risk levels (CRITICAL, HIGH, MEDIUM, LOW, CLEAR)
- **Batch Screening** — Screen hundreds of entities in a single API call
- **Entity Type Filtering** — Filter by individual, company, vessel, or aircraft
- **International Sanctions** — Optionally check EU, UN, UK, and 40+ other lists via OpenSanctions
- **Smart False Positive Reduction** — Strips business suffixes (Inc, LLC, Corp) before matching
- **AI Agent Compatible** — Works with Claude, GPT, CrewAI, and LangChain via Apify MCP Server
- **Structured JSON Output** — Programs, addresses, IDs, aliases, vessel info — ready for compliance workflows

## Quick Start

### Using the Apify API (Node.js)

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });

const run = await client.actor('george.the.developer/ofac-sanctions-screener').call({
    queries: ['Bank Melli Iran', 'Gazprombank', 'Apple Inc'],
    matchThreshold: 70,
    includeAliases: true,
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(JSON.stringify(items, null, 2));
```

### Using the Apify API (Python)

```python
from apify_client import ApifyClient

client = ApifyClient('YOUR_APIFY_TOKEN')

run = client.actor('george.the.developer/ofac-sanctions-screener').call(run_input={
    'queries': ['Bank Melli Iran', 'Gazprombank', 'Apple Inc'],
    'matchThreshold': 70,
    'includeAliases': True,
})

for item in client.dataset(run['defaultDatasetId']).iterate_items():
    print(f"{item['queryName']}: {item['riskLevel']} (confidence: {item.get('matchConfidence', 'N/A')}%)")
```

### Using cURL

```bash
curl -X POST "https://api.apify.com/v2/acts/george.the.developer~ofac-sanctions-screener/runs?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["Bank Melli Iran", "Gazprombank", "Apple Inc"],
    "matchThreshold": 70,
    "includeAliases": true
  }'
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `queries` | string[] | Yes | — | Entity names to screen (company names, person names, vessel names) |
| `matchThreshold` | integer | No | 70 | Minimum fuzzy match confidence (0-100). 70+ recommended for compliance |
| `entityType` | string | No | `all` | Filter: `all`, `individual`, `entity`, `vessel`, `aircraft` |
| `includeOpenSanctions` | boolean | No | `false` | Also check EU, UN, UK sanctions via OpenSanctions API |
| `maxMatchesPerQuery` | integer | No | 5 | Max matching entries returned per query (1-25) |
| `includeAliases` | boolean | No | `true` | Match against known aliases (AKAs) of sanctioned entities |

## Output Example

### Sanctioned Entity Match

```json
{
    "queryName": "Bank Melli Iran",
    "matchedName": "BANK MELLI IRAN",
    "matchConfidence": 100,
    "sanctionsList": "OFAC SDN",
    "entityType": "entity",
    "sdnUid": 25578,
    "programs": ["IFSR", "IRAN", "SDGT"],
    "aliases": ["BANK MELLI", "MELLI BANK", "NATIONAL BANK OF IRAN", "BMI"],
    "addresses": [{"city": "Tehran", "country": "Iran"}],
    "riskLevel": "CRITICAL",
    "sdnListDate": "03/09/2026",
    "screenedAt": "2026-03-11T12:00:00.000Z",
    "source": "US Treasury OFAC SDN List"
}
```

### Clear Entity (No Match)

```json
{
    "queryName": "Apple Inc",
    "matchedName": null,
    "matchConfidence": 0,
    "riskLevel": "CLEAR",
    "result": "NO_MATCH",
    "message": "No sanctions matches found for \"Apple Inc\" above 70% confidence threshold.",
    "source": "US Treasury OFAC SDN List"
}
```

See [`sample-output.json`](sample-output.json) for a complete multi-entity output example.

## Use Cases

### KYC/AML Onboarding
Banks, fintech companies, and payment processors can batch-screen customers during onboarding. Screen hundreds of entities in one API call for automated KYC compliance.

### Trade Compliance
Screen suppliers, buyers, and freight forwarders before every international shipment. Stay compliant with OFAC regulations and avoid penalties up to $20 million per violation.

### Vendor & Partner Screening
Verify business partners, investors, or acquisition targets against the SDN sanctions list before signing contracts or processing payments.

### Supply Chain Risk Management
Monitor your entire supplier network for sanctions exposure. Schedule daily or weekly runs to catch new OFAC designations as they happen.

### AI Agent Integration
Connect via the Apify MCP Server so AI agents (Claude Code, CrewAI, LangChain, AutoGPT) can automatically screen entities as part of automated compliance pipelines. See [`examples/mcp-integration.md`](examples/mcp-integration.md).

### Investor & Portfolio Screening
Check portfolio companies and their officers against OFAC, especially relevant during active sanctions campaigns with frequent new designations.

## Pricing

| Event | Cost |
|-------|------|
| Per entity screened | **$0.01** |
| Run start | **$0.005** |

Screen **100 entities for $1.00**. No monthly fees, no contracts, no minimums.

Enterprise sanctions screening tools charge **$5,000 - $100,000+/year**. This does the same job using the same official OFAC data at a fraction of the cost.

## How It Works

1. Downloads the official OFAC SDN XML file from the US Treasury (~15MB, refreshed daily)
2. Parses all 18,000+ sanctioned entries including names, aliases, addresses, and IDs
3. Builds a fuzzy search index using Fuse.js for fast approximate matching
4. Strips common business suffixes (Inc, LLC, Corp, etc.) to reduce false positives
5. Computes confidence scores using Dice coefficient + Fuse.js ranking
6. Caches the parsed SDN list for 24 hours to speed up repeated runs
7. Optionally queries the OpenSanctions API for international sanctions (EU, UN, UK)

## Data Sources

- **OFAC SDN List** — Official US Treasury Specially Designated Nationals list: [treasury.gov/ofac/downloads/sdn.xml](https://www.treasury.gov/ofac/downloads/sdn.xml)
- **OpenSanctions** (optional) — Aggregated international sanctions from EU, UN, UK, and 40+ jurisdictions: [opensanctions.org](https://opensanctions.org)

## More Examples

- [Node.js API example](examples/nodejs-api.js)
- [Python API example](examples/python-api.py)
- [MCP / AI Agent integration](examples/mcp-integration.md)

## Also Available on RapidAPI

Prefer a standard REST API? This screener is also available on **[RapidAPI](https://rapidapi.com/georgethedeveloper3046/api/ofac-sanctions-screener-api)** with simple API key authentication:

- **Free tier**: 50 requests/month
- **Pro**: $39/month (1,000 requests)
- **Ultra**: $99/month (5,000 requests)
- **Mega**: $249/month (20,000 requests)

## Links

- **Run this actor**: [apify.com/george.the.developer/ofac-sanctions-screener](https://apify.com/george.the.developer/ofac-sanctions-screener)
- **Also on RapidAPI**: [rapidapi.com/georgethedeveloper3046/api/ofac-sanctions-screener-api](https://rapidapi.com/georgethedeveloper3046/api/ofac-sanctions-screener-api)
- **Apify API docs**: [docs.apify.com/api/v2](https://docs.apify.com/api/v2)
- **OFAC SDN List info**: [treasury.gov/ofac](https://www.treasury.gov/ofac)

---

**Built by [The AI Entrepreneur](https://github.com/the-ai-entrepreneur-ai-hub)** — Automated compliance tools for the modern enterprise.
