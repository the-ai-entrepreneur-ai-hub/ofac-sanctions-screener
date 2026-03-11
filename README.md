# OFAC Sanctions Screener

[![Run on Apify](https://img.shields.io/badge/Run_on-Apify-00C48C?logo=apify)](https://apify.com/george.the.developer/ofac-sanctions-screener)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Screen companies, individuals, and vessels against the **US Treasury OFAC SDN (Specially Designated Nationals) sanctions list**. Uses fuzzy matching with configurable thresholds to catch name variations, transliterations, and aliases across 18,000+ sanctioned entities. Returns structured risk assessments with confidence scores, sanction programs, addresses, and aliases.

---

## Quick Start

### cURL

```bash
curl "https://api.apify.com/v2/acts/george.the.developer~ofac-sanctions-screener/run-sync-get-dataset-items?token=YOUR_API_TOKEN" \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["Bank Melli Iran", "Huawei Technologies"],
    "matchThreshold": 70
  }'
```

### Node.js

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_API_TOKEN' });

const run = await client.actor('george.the.developer/ofac-sanctions-screener').call({
    queries: ['Bank Melli Iran', 'Huawei Technologies', 'Apple Inc'],
    matchThreshold: 70,
    entityType: 'all',
});

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
    console.log(`${item.queryName}: ${item.riskLevel} (${item.matchConfidence}% confidence)`);
}
```

### Python

```python
from apify_client import ApifyClient

client = ApifyClient('YOUR_API_TOKEN')

run = client.actor('george.the.developer/ofac-sanctions-screener').call(run_input={
    'queries': ['Bank Melli Iran', 'Huawei Technologies', 'Apple Inc'],
    'matchThreshold': 70,
    'entityType': 'all',
})

for item in client.dataset(run['defaultDatasetId']).iterate_items():
    print(f"{item['queryName']}: {item['riskLevel']} ({item['matchConfidence']}% confidence)")
```

---

## What You Get

Each screened entity returns:

| Field | Description |
|-------|-------------|
| `queryName` | The name you submitted for screening |
| `matchedName` | Matched SDN list entry (or `null` if clear) |
| `matchConfidence` | 0-100 confidence score |
| `riskLevel` | `CRITICAL`, `HIGH`, `MEDIUM`, or `CLEAR` |
| `sanctionsList` | Source list (e.g., "OFAC SDN") |
| `entityType` | `individual`, `entity`, or `vessel` |
| `programs` | Sanction programs (IRAN, SDGT, UKRAINE-EO13661, etc.) |
| `aliases` | Known aliases and alternate names |
| `addresses` | Associated addresses with city/country |
| `sdnUid` | Unique SDN list identifier |
| `screenedAt` | ISO timestamp of the screening |

See [`sample-output.json`](sample-output.json) for a full example.

---

## Use Cases

- **KYC/AML Compliance** - Screen customers and counterparties before onboarding
- **Vendor & Supplier Due Diligence** - Check business partners against sanctions
- **Trade Compliance** - Verify export/import counterparties for ITAR/EAR
- **Investment Screening** - Screen portfolio companies and fund investors
- **Insurance Underwriting** - Check policyholders against denied-party lists
- **Real Estate Transactions** - Screen buyers per FinCEN requirements
- **Batch Screening** - Process thousands of entities in a single API call

---

## Pricing

**$0.01 per entity screened** (pay-per-event). No monthly fees, no minimums.

Screen 100 entities = $1.00. Free tier available on Apify for testing.

---

## AI Agent Integration

This actor works as a tool for AI agents via the [Apify MCP Server](https://docs.apify.com/platform/integrations/mcp-server). Any AI framework that supports MCP (Claude, CrewAI, LangChain, etc.) can use it directly.

Add to your MCP config (`claude_desktop_config.json`, `mcp.json`, etc.):

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/apify-mcp-server"],
      "env": {
        "APIFY_TOKEN": "YOUR_API_TOKEN"
      }
    }
  }
}
```

See [`integrations/`](integrations/) for CrewAI and MCP config examples.

---

## Links

- [Run on Apify Store](https://apify.com/george.the.developer/ofac-sanctions-screener)
- [API Documentation](https://docs.apify.com/api/v2)
- [Report Issues](https://github.com/the-ai-entrepreneur-ai-hub/ofac-sanctions-screener/issues)

## Related Tools

- [Entity OSINT Enricher](https://github.com/the-ai-entrepreneur-ai-hub/entity-osint-enricher) - Combine OFAC screening with corporate registry lookups, news monitoring, and contact extraction
- [Shipping Disruption Tracker](https://github.com/the-ai-entrepreneur-ai-hub/shipping-disruption-tracker) - Monitor shipping chokepoints (Hormuz, Suez, Red Sea) for trade risk assessment

---

## License

[MIT](LICENSE)
