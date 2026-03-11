"""
OFAC Sanctions Screener — Python API Example

Screen entities against the US Treasury OFAC SDN sanctions list
using the Apify Python client.

Install: pip install apify-client
Run:     python python-api.py

Get your API token at: https://console.apify.com/account/integrations
Actor:   https://apify.com/george.the.developer/ofac-sanctions-screener
"""

from apify_client import ApifyClient

client = ApifyClient('YOUR_APIFY_TOKEN')

# Entities to screen against the OFAC SDN sanctions list
run_input = {
    'queries': [
        'Bank Melli Iran',       # Known sanctioned entity
        'Gazprombank',           # Known sanctioned entity
        'Rosneft Oil Company',   # Known sanctioned entity
        'Apple Inc',             # Should return CLEAR
        'Microsoft Corporation', # Should return CLEAR
    ],
    'matchThreshold': 70,      # Minimum confidence score (70+ recommended)
    'includeAliases': True,    # Also match against known aliases (AKAs)
    'entityType': 'all',       # Filter: all, individual, entity, vessel, aircraft
    'maxMatchesPerQuery': 5,   # Max matches per entity
}

print(f"Screening {len(run_input['queries'])} entities against OFAC SDN list...\n")

run = client.actor('george.the.developer/ofac-sanctions-screener').call(run_input=run_input)

print(f"Run finished. Status: {run['status']}")
print(f"Dataset ID: {run['defaultDatasetId']}\n")

# Fetch and display results
for item in client.dataset(run['defaultDatasetId']).iterate_items():
    risk = item.get('riskLevel', 'UNKNOWN')
    confidence = item.get('matchConfidence', 0)
    query = item['queryName']

    if risk == 'CLEAR':
        print(f"  CLEAR   | {query} — no sanctions match")
    else:
        matched = item.get('matchedName', 'N/A')
        programs = ', '.join(item.get('programs', []))
        print(f"  {risk:8s} | {query} — {confidence}% match to \"{matched}\"")
        print(f"           | Programs: {programs}")
        aliases = item.get('aliases', [])
        if aliases:
            print(f"           | Aliases: {', '.join(aliases[:3])}")

    print()

# Tip: For production KYC/AML workflows, save results to your database
# and flag any entity with riskLevel != 'CLEAR' for manual review.
